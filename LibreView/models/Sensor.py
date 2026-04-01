from dataclasses import dataclass
from dataclass_wizard import JSONWizard


@dataclass
class Sensor(JSONWizard):
    """Represents a glucose sensor.

    Contains sensor identification, calibration parameters, and status flags.
    """

    device_id: str
    sn: str
    a: int
    w: int
    pt: int
    s: bool
    lj: bool
