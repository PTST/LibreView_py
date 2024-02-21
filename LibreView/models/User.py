from dataclasses import dataclass
from typing import Any, List, Dict
from uuid import UUID
from dataclass_wizard import JSONWizard
from LibreView.models.Device import Device
from LibreView.models.Practice import Practice


@dataclass
class User(JSONWizard):
    id: UUID
    first_name: str
    last_name: str
    email: str
    country: str
    ui_language: str
    communication_language: str
    account_type: str
    uom: int
    date_format: int
    time_format: int
    email_day: List[int]
    created: int
    last_login: int
    date_of_birth: int
    practices: Dict[UUID, Practice]
    devices: Dict[str, Device]
