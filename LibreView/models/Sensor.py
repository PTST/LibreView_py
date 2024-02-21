from dataclasses import dataclass
from dataclass_wizard import JSONWizard


@dataclass
class Sensor(JSONWizard):
    device_id: str
    sn: str
    a: int
    w: int
    pt: int
    s: bool
    lj: bool
