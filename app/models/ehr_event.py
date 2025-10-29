from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict

class EHREvent(BaseModel):
    patient_id: str
    abha_id: Optional[str]
    event_type: str
    timestamp: datetime
    meta: Optional[Dict[str, str]] = None
