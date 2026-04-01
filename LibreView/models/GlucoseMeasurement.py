from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from dataclass_wizard import JSONWizard, json_field


@dataclass
class GlucoseMeasurement(JSONWizard):
    """Represents a single glucose measurement reading.

    Contains glucose levels, trends, timestamps, and metadata about the measurement.
    Timestamps are parsed from the API's string format to Python datetime objects.
    """

    type: int
    value_in_mg_per_dl: int
    measurement_color: int
    glucose_units: int
    value: float
    is_high: bool
    is_low: bool
    _factory_timestamp: str = json_field("FactoryTimestamp")  # type: ignore
    _timestamp: str = json_field("Timestamp")  # type: ignore
    trend_arrow: Optional[int] = None
    trend_message: Optional[str] = None

    @property
    def factory_timestamp(self) -> datetime:
        """Parse and return the factory timestamp as a datetime object.

        Returns:
            datetime: The factory timestamp in UTC.
        """
        return self.parse_dt(self._factory_timestamp)

    @property
    def timestamp(self) -> datetime:
        """Parse and return the measurement timestamp as a datetime object.

        Returns:
            datetime: The measurement timestamp in UTC.
        """
        return self.parse_dt(self._timestamp)

    def parse_dt(self, val: str) -> datetime:
        """Parse a timestamp string from the API format to datetime.

        Args:
            val: Timestamp string in format 'M/D/YYYY h:MM:SS AM/PM'.

        Returns:
            datetime: Parsed datetime object.
        """
        splitted = val.split("/")
        splitted[0] = splitted[0].zfill(2)
        splitted[1] = splitted[1].zfill(2)
        return datetime.strptime("/".join(splitted), "%m/%d/%Y %I:%M:%S %p")
