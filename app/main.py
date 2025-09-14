import os
from typing import Optional, Tuple
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from app.services.prompts import compose_prompt, prompt_hash
from app.services.jobs import JobStore, JobRecord
from app.services.video_generator import VideoGenerator
from app.services.prompt_optimizer import optimize_prompt
from app.services.feedback import save_feedback

APP_ORIGIN = os.getenv("APP_ORIGIN", "*")
PROVIDER_NAME = os.getenv("VIDEO_PROVIDER", "replicate").lower()

app = FastAPI(title="Peppo AI – Video Generator", version="1.2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[APP_ORIGIN] if APP_ORIGIN != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

job_store = JobStore()
video_gen = VideoGenerator(PROVIDER_NAME)  # 👈 central entrypoint

@app.get("/healthz")
def healthz():
    return {"ok": True, "provider": PROVIDER_NAME}

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate(payload: dict):
    user_prompt = (payload.get("prompt") or "").strip()
    style = (payload.get("style") or "cinematic").strip().lower()
    if not user_prompt:
        raise HTTPException(400, "Prompt is required")

    h = prompt_hash(user_prompt, style)
    cached = job_store.get_by_hash(h)
    if cached and cached.status == "succeeded":
        return {
            "job_id": cached.job_id,
            "status": "succeeded",
            "video_url": cached.video_path,
            "cached": True
        }

    final_prompt = compose_prompt(user_prompt, style)
    job = video_gen.submit(final_prompt, style=style)

    rec = JobRecord(
        job_id=job.job_id,
        status=job.status,
        video_path=None,
        provider=PROVIDER_NAME,
        prompt_hash=h
    )
    job_store.put(rec)
    return {"job_id": job.job_id, "status": job.status, "cached": False}

@app.get("/status/{job_id}")
async def status(job_id: str):
    pj = video_gen.fetch(job_id)
    rec = job_store.get(job_id)
    if not rec:
        raise HTTPException(404, "Job not found")

    rec.status = pj.status
    if pj.status == "succeeded" and not rec.video_path:
        rec.video_path = f"/video/{job_id}"
        if pj.video_url:
            rec.meta["provider_output_url"] = pj.video_url

    if pj.error:
        return {"job_id": job_id, "status": "failed", "error": pj.error}

    return {
        "job_id": job_id,
        "status": rec.status,
        "video_url": rec.video_path,
        "cached": rec.cached
    }

def _parse_range(range_header: Optional[str], file_size: int) -> Optional[Tuple[int,int]]:
    if not range_header or "=" not in range_header:
        return None
    units, rng = range_header.split("=", 1)
    if units.strip().lower() != "bytes":
        return None
    start_s, _, end_s = rng.partition("-")
    try:
        if start_s and end_s:
            start, end = int(start_s), int(end_s)
        elif start_s:
            start, end = int(start_s), file_size - 1
        else:
            n = int(end_s)
            start, end = file_size - n, file_size - 1
        if start < 0 or end >= file_size or start > end:
            return None
        return (start, end)
    except ValueError:
        return None

@app.get("/video/{job_id}")
def video(job_id: str, request: Request):
    # Check if we have a generated video from the provider
    rec = job_store.get(job_id)
    if rec and rec.status == "succeeded" and rec.meta.get("provider_output_url"):
        # Redirect to the actual video URL from Replicate
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url=rec.meta["provider_output_url"])
    
    # Fallback to placeholder video
    path = "app/static/placeholder.mp4"
    if not os.path.exists(path):
        raise HTTPException(404, "Video missing")

    file_size = os.path.getsize(path)
    range_header = request.headers.get("range")
    rng = _parse_range(range_header, file_size)

    def iterfile(start: int = 0, end: int = file_size - 1, chunk_size: int = 64 * 1024):
        with open(path, "rb") as f:
            f.seek(start)
            bytes_left = end - start + 1
            while bytes_left > 0:
                chunk = f.read(min(chunk_size, bytes_left))
                if not chunk:
                    break
                bytes_left -= len(chunk)
                yield chunk

    if rng:
        start, end = rng
        headers = {
            "Content-Range": f"bytes {start}-{end}/{file_size}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(end - start + 1),
        }
        return StreamingResponse(iterfile(start, end), status_code=206, headers=headers, media_type="video/mp4")

    headers = {"Accept-Ranges": "bytes", "Content-Length": str(file_size)}
    return StreamingResponse(iterfile(), headers=headers, media_type="video/mp4")

@app.post("/optimize_prompt")
async def optimize(payload: dict):
    user_prompt = (payload.get("prompt") or "").strip()
    style = (payload.get("style") or "cinematic").strip().lower()

    if not user_prompt:
        raise HTTPException(400, "Prompt is required")

    optimized = optimize_prompt(user_prompt, style)
    return {"optimized_prompt": optimized}

@app.post("/feedback")
async def feedback(payload: dict):
    video_id = payload.get("video_id")
    liked = payload.get("liked")

    if not video_id or liked is None:
        raise HTTPException(400, "video_id and liked are required")

    res = save_feedback(video_id, bool(liked))
    return res
