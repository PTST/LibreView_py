from datetime import datetime
import os
from uuid import UUID
from LibreView import LibreView
from LibreView.models import Connection, GlucoseMeasurement, Sensor

USERNAME: str = os.environ["libre_username"]
PASSWORD: str = os.environ["libre_password"]


def test_connections():
    libre = LibreView(USERNAME, PASSWORD)
    cons = libre.get_connections()
    assert len(cons) > 0
    con = cons[0]
    assert isinstance(con, Connection)
    assert isinstance(con.id, UUID)
    assert isinstance(con.patient_id, UUID)
    assert isinstance(con.country, str)
    assert isinstance(con.status, int)
    assert isinstance(con.first_name, str)
    assert isinstance(con.last_name, str)
    assert isinstance(con.target_low, int)
    assert isinstance(con.target_high, int)
    assert isinstance(con.uom, int)

    assert isinstance(con.sensor, Sensor)
    assert isinstance(con.glucose_measurement, GlucoseMeasurement)

    sensor = con.sensor
    assert isinstance(sensor.device_id, str)
    assert isinstance(sensor.sn, str)
    assert isinstance(sensor.a, int)
    assert isinstance(sensor.w, int)
    assert isinstance(sensor.pt, int)
    assert isinstance(sensor.s, bool)
    assert isinstance(sensor.lj, bool)

    gm = con.glucose_measurement
    assert isinstance(gm.type, int)
    assert isinstance(gm.value_in_mg_per_dl, int)
    assert isinstance(gm.trend_arrow, int)
    assert isinstance(gm.measurement_color, int)
    assert isinstance(gm.glucose_units, int)
    assert isinstance(gm.value, float)
    assert isinstance(gm.is_high, bool)
    assert isinstance(gm.is_low, bool)
    assert isinstance(gm.factory_timestamp, datetime)
    assert isinstance(gm.timestamp, datetime)
    assert isinstance(gm.trend_message, str) or gm.trend_message is None
