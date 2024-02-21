from dataclasses import dataclass
from uuid import UUID
from dataclass_wizard import JSONWizard


@dataclass
class Device(JSONWizard):
    id: UUID
    nickname: str
    sn: UUID
    type: int
    upload_date: int
