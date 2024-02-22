from typing import List
from LibreView.models import Connection
from LibreView.utils import API


class LibreView:
    client: API

    def __init__(self, username: str, password: str):
        self.client = API(username, password)

    def get_connections(self) -> List[Connection]:
        return self.client.get_connections()
