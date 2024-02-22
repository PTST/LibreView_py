from dataclasses import dataclass
from uuid import UUID
from dataclass_wizard import JSONWizard

# from LibreView.models import Sensor, GlucoseMeasurement
from LibreView.models.GlucoseMeasurement import GlucoseMeasurement
from LibreView.models.Sensor import Sensor


@dataclass
class Connection(JSONWizard):
    id: UUID
    patient_id: UUID
    country: str
    status: int
    first_name: str
    last_name: str
    target_low: int
    target_high: int
    uom: int
    sensor: Sensor
    glucose_measurement: GlucoseMeasurement
