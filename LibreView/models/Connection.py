from dataclasses import dataclass
from uuid import UUID
from dataclass_wizard import JSONWizard
from LibreView.models.Sensor import Sensor
from LibreView.models.GlucoseMeasurement import GlucoseMeasurement


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
