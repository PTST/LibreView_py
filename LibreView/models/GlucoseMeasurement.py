from dataclasses import dataclass
from datetime import datetime
from dataclass_wizard import JSONWizard, json_field


@dataclass
class GlucoseMeasurement(JSONWizard):
    _timestamp: str
    type: int
    value_in_mg_per_dl: int
    trend_arrow: int
    measurement_color: int
    glucose_units: int
    value: float
    is_high: bool
    is_low: bool
    _factory_timestamp: str = json_field("FactoryTimestamp")  # type: ignore

    @property
    def factory_timestamp(self) -> datetime:
        return self.parse_dt(self._factory_timestamp)

    _timestamp: str = json_field("Timestamp")  # type: ignore

    @property
    def timestamp(self) -> datetime:
        return self.parse_dt(self._timestamp)

    trend_message: str | None = None

    def parse_dt(self, val: str) -> datetime:
        splitted = val.split("/")
        splitted[0] = splitted[0].zfill(2)
        splitted[1] = splitted[1].zfill(2)
        return datetime.strptime("/".join(splitted), "%m/%d/%Y %I:%M:%S %p")
