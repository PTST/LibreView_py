from typing import Dict, List, Optional
from uuid import UUID
from LibreView.models import Connection
from LibreView.utils import API


class LibreView:
    client: API

    connections_dict: Dict[UUID, Connection]

    def __init__(self, username: str, password: str, region: Optional[str] = None):
        self.client = API(username, password, region)

    def get_connections(self) -> List[Connection]:
        cons = self.client.get_connections()
        self.connections_dict = {x.id: x for x in cons}
        return cons
