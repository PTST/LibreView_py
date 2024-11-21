from dataclasses import dataclass
from uuid import UUID
from dataclass_wizard import JSONWizard


@dataclass
class Practice(JSONWizard):
    id: UUID
    practice_id: str
    name: str
    address1: str
    city: str
    state: str
    zip: str
    phone_number: str
    address2: str | None = None
