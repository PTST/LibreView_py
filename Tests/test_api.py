from datetime import datetime
import os
from uuid import UUID
import LibreView
import logging

LOGGER = logging.getLogger(__name__)
USERNAME: str = os.environ["libre_username"]
PASSWORD: str = os.environ["libre_password"]


def test_logon():
    api = LibreView.API(USERNAME, PASSWORD)
    assert api.client.headers.get("Authorization") != None


def test_get_user():
    api = LibreView.API(USERNAME, PASSWORD)
    usr = api.get_user()
    assert isinstance(usr.first_name, str)
    assert len(usr.first_name) > 0


def test_get_connections():
    api = LibreView.API(USERNAME, PASSWORD)
    cons = api.get_connections()
    assert len(cons) > 0
    con = cons[0]
    assert isinstance(con.patient_id, UUID)
    assert isinstance(con.glucose_measurement.timestamp, datetime)
    assert len(con.first_name) > 0
