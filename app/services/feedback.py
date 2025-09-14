import os
from datetime import datetime

FEEDBACK_FILE = os.path.join("app", "user_feedback.txt")

def save_feedback(video_id: str, liked: bool):
    """
    Append a feedback entry to app/user_feedback.txt
    Format: 2025-08-23 12:10 | video_id=abc123 | liked=True
    """
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{ts} | video_id={video_id} | liked={liked}\n"

    # Ensure directory exists
    os.makedirs(os.path.dirname(FEEDBACK_FILE), exist_ok=True)

    with open(FEEDBACK_FILE, "a", encoding="utf-8") as f:
        f.write(line)

    return {"ok": True, "message": "Feedback saved"}
