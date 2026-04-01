from dataclasses import dataclass
from uuid import UUID
from dataclass_wizard import JSONWizard


@dataclass
class Device(JSONWizard):
    """Represents a glucose monitoring device.

    Contains device identification, type, and upload timestamp.
    """

    id: UUID
    nickname: str
    sn: UUID
    type: int
    upload_date: int
