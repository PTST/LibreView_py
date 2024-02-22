from datetime import datetime
import os
from uuid import UUID
from LibreView.models import Connection, Device, GlucoseMeasurement, Practice, Sensor
from LibreView.utils.API import API
import logging

LOGGER = logging.getLogger(__name__)
USERNAME: str = os.environ["libre_username"]
PASSWORD: str = os.environ["libre_password"]


def test_logon():
    api = API(USERNAME, PASSWORD)
    assert api.client.headers.get("Authorization") != None


def test_get_user():
    api = API(USERNAME, PASSWORD)
    usr = api.get_user()
    assert isinstance(usr.id, UUID)
    assert isinstance(usr.first_name, str)
    assert isinstance(usr.last_name, str)
    assert isinstance(usr.email, str)
    assert isinstance(usr.country, str)
    assert isinstance(usr.ui_language, str)
    assert isinstance(usr.communication_language, str)
    assert isinstance(usr.account_type, str)
    assert isinstance(usr.uom, int)
    assert isinstance(usr.date_format, int)
    assert isinstance(usr.time_format, int)
    assert isinstance(usr.email_day, list)
    assert isinstance(usr.created, int)
    assert isinstance(usr.last_login, int)
    assert isinstance(usr.date_of_birth, int)
    assert isinstance(usr.practices, dict)
    assert isinstance(usr.devices, dict)

    for key, practice in usr.practices.items():
        assert isinstance(key, UUID)
        assert isinstance(practice, Practice)
        assert isinstance(practice.id, UUID)
        assert isinstance(practice.practice_id, str)
        assert isinstance(practice.name, str)
        assert isinstance(practice.address1, str)
        assert isinstance(practice.city, str)
        assert isinstance(practice.state, str)
        assert isinstance(practice.zip, str)
        assert isinstance(practice.phone_number, str)
        assert isinstance(practice.address2, str) or practice.address2 is None

    for key, device in usr.devices.items():
        assert isinstance(key, str)
        assert isinstance(device, Device)
        assert isinstance(device.id, UUID)
        assert isinstance(device.nickname, str)
        assert isinstance(device.sn, UUID)
        assert isinstance(device.type, int)
        assert isinstance(device.upload_date, int)


def test_get_connections():
    api = API(USERNAME, PASSWORD)
    cons = api.get_connections()
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
