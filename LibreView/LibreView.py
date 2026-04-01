from typing import Dict, List, Optional
from uuid import UUID
from LibreView.models import Connection, GlucoseMeasurement
from LibreView.utils import API


class LibreView:
    """High-level client for accessing LibreView glucose monitoring data.

    Provides methods to authenticate, retrieve connections (patients), and access
    glucose measurements. Caches connections for efficient access.
    """

    def __init__(
        self, username: str, password: str, region: Optional[str] = None
    ) -> None:
        """Initialize the LibreView client.

        Args:
            username: The email/username for API authentication.
            password: The password for API authentication.
            region: Optional region code for the API endpoint.
        """
        self.client = API(username, password, region)
        self.connections_dict: Dict[UUID, Connection] = {}

    def get_connections(self) -> List[Connection]:
        """Retrieve all connections and cache them locally.

        Returns:
            A list of Connection objects representing accessible patients.
        """
        cons = self.client.get_connections()
        self.connections_dict = {x.id: x for x in cons}
        return cons

    def get_graph_from_connection(
        self, connection: Connection
    ) -> list[GlucoseMeasurement]:
        """Get glucose measurement data for a specific connection.

        Args:
            connection: The Connection object for the patient.

        Returns:
            A list of GlucoseMeasurement objects for the patient.
        """
        return self.client.get_graph(connection.patient_id)
