import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from app.services.jobs import JobRecord, JobStore
from app.services.prompts import compose_prompt, prompt_hash
from app.providers.base import BaseProvider
from app.providers.mock import MockProvider
from app.providers.modelslab import ModelsLabProvider
from app.providers.replicate import ReplicateProvider

# Load environment variables
load_dotenv()

# Global envs
PROVIDER_NAME = os.getenv("VIDEO_PROVIDER", "replicate").lower()
job_store = JobStore()


def _build_provider() -> BaseProvider:
    """Factory to select provider based on env"""
    if PROVIDER_NAME == "replicate":
        return ReplicateProvider()
    elif PROVIDER_NAME == "modelslab":
        return ModelsLabProvider()
    elif PROVIDER_NAME == "mock":
        return MockProvider()
    return ReplicateProvider()  # Default to Replicate


class VideoGenerator:
    """Handles video generation lifecycle across providers."""

    def __init__(self, provider: Optional[BaseProvider] = None):
        # provider can be passed in or built based on env
        if isinstance(provider, str):
            # if someone passes "replicate"/"modelslab"/"mock"
            if provider == "replicate":
                self.provider = ReplicateProvider()
            elif provider == "modelslab":
                self.provider = ModelsLabProvider()
            elif provider == "mock":
                self.provider = MockProvider()
            else:
                self.provider = ReplicateProvider()  # Default to Replicate
        else:
            self.provider = provider or _build_provider()

    def submit(
        self,
        user_prompt: str,
        style: str = "cinematic",
        options: Optional[Dict[str, Any]] = None,
    ):
        """
        Submit a video generation request.
        Returns a ProviderJob object with job_id, status, etc.
        """
        if not user_prompt.strip():
            raise ValueError("Prompt is required")

        h = prompt_hash(user_prompt, style)
        cached = job_store.get_by_hash(h)

        if cached and cached.status == "succeeded":
            return cached  # return JobRecord directly

        final_prompt = compose_prompt(user_prompt, style)
        job = self.provider.submit(final_prompt, options={"style": style, **(options or {})})

        rec = JobRecord(
            job_id=job.job_id,
            status=job.status,
            video_path=None,
            provider=PROVIDER_NAME,
            prompt_hash=h,
        )
        job_store.put(rec)
        return job

    def fetch(self, job_id: str):
        """
        Check job status and update store.
        Returns a ProviderJob with latest status.
        """
        pj = self.provider.fetch(job_id)
        rec = job_store.get(job_id)

        if not rec:
            return pj

        rec.status = pj.status
        if pj.status == "succeeded" and not rec.video_path:
            rec.video_path = f"/video/{job_id}"
            if pj.video_url:
                rec.meta["provider_output_url"] = pj.video_url

        return pj
