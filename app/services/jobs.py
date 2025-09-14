from typing import Dict, Optional
from dataclasses import dataclass, field

@dataclass
class JobRecord:
    job_id: str
    status: str
    video_path: Optional[str]  # local path or URL served to UI
    provider: str
    prompt_hash: str
    cached: bool = False
    meta: Dict[str, str] = field(default_factory=dict)  # provider details (e.g., actual output URL)

class JobStore:
    def __init__(self):
        self._by_id: Dict[str, JobRecord] = {}
        self._by_hash: Dict[str, JobRecord] = {}

    def get_by_hash(self, h: str) -> Optional[JobRecord]:
        return self._by_hash.get(h)

    def put(self, rec: JobRecord):
        self._by_id[rec.job_id] = rec
        self._by_hash[rec.prompt_hash] = rec

    def get(self, job_id: str) -> Optional[JobRecord]:
        return self._by_id.get(job_id)
