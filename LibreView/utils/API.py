from typing import Optional, Any, Callable
from uuid import UUID
import requests
from LibreView.models import User, Connection, GlucoseMeasurement
from hashlib import sha256


def reauth_on_fail(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator that retries a function with reauthentication on 401 errors.
    
    Args:
        func: The function to wrap. Expected to be a method of the API class.
        
    Returns:
        A wrapper function that catches 401 HTTPErrors and retries after authentication.
    """
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except requests.HTTPError as e:
            if e.response.status_code == 401:
                api: API = args[0]
                api.authenticate()
                return func(*args, **kwargs)
            raise e
    return wrapper


class API:
    """Client for interacting with the LibreView API.
    
    Handles authentication, token management, and API requests for user data,
    connections, and glucose measurements.
    """
    
    def __init__(self, username: str, password: str, region: Optional[str] = None) -> None:
        """Initialize the API client.
        
        Args:
            username: The email/username for API authentication.
            password: The password for API authentication.
            region: Optional region code (e.g., 'us', 'eu') for region-specific API endpoint.
        """
        self.base_url = "https://api.libreview.io"
        if region:
            self.base_url = f"https://api-{region}.libreview.io"
        self.client = requests.session()
        self.product = "llu.android"
        self.version = "4.16.0"
        self.username = username
        self.password = password
        self.client.headers["product"] = self.product
        self.client.headers["version"] = self.version

    @property
    def missing_auth_header(self) -> bool:
        """Check if the client is missing an Authorization header.
        
        Returns:
            True if Authorization header is missing, False otherwise.
        """
        return self.client.headers.get("Authorization") is None

    def authenticate(self) -> None:
        """Authenticate with the LibreView API and set authorization headers.
        
        Handles region redirects, term acceptance, and sets the account ID and token.
        
        Raises:
            Exception: If authentication fails or an unknown error occurs.
        """
        r = self.client.post(
            f"{self.base_url}/llu/auth/login",
            json={
                "email": self.username,
                "password": self.password,
            },
        )
        r.raise_for_status()
        content = r.json()

        if (
            content
            and content.get("status") == 0
            and content["data"].get("redirect", False)
        ):
            region = content["data"]["region"]
            self.base_url = f"https://api-{region}.libreview.io"
            return self.authenticate()

        # status 0 == login successfull
        if content and content.get("status") == 0:
            account_id = content["data"]["user"]["id"]
            self.client.headers["account-id"] = sha256(
                account_id.encode("utf-8")
            ).hexdigest()
            self.set_token(content["data"]["authTicket"]["token"])
            return

        # status 4 == missing term accepts
        if content and content.get("status") == 4:
            self.accept_terms(content["data"]["authTicket"]["token"])
            return

        error = "Unknown error occured during authentication"
        if content and content.get("error") and content["error"].get("message"):
            error = content["error"]["message"]

        raise Exception(error)

    def set_token(self, token: str) -> None:
        """Set the authorization token in the client headers.
        
        Args:
            token: The authentication token from the API.
        """
        self.client.headers["Authorization"] = f"Bearer {token}"

    def accept_terms(self, token: str) -> None:
        """Accept terms and conditions with the given authentication token.
        
        Args:
            token: The authentication token to use for the request.
        """
        if (self.missing_auth_header):
            self.authenticate()

        r = self.client.post(
            f"{self.base_url}/llu/auth/login",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )
        r.raise_for_status()
        content = r.json()
        if content and content.get("status") == 0:
            account_id = content["data"]["user"]["id"]
            self.client.headers["account-id"] = sha256(
                account_id.encode("utf-8")
            ).hexdigest()
            self.set_token(content["data"]["authTicket"]["token"])
            return

    @reauth_on_fail
    def get_user(self) -> User:
        """Get the authenticated user's information.
        
        Returns:
            A User object containing the user's data.
            
        Raises:
            requests.HTTPError: If the API request fails.
        """
        if (self.missing_auth_header):
            self.authenticate()

        r = self.client.get(
            f"{self.base_url}/user",
        )
        r.raise_for_status()
        return User.from_dict(r.json()["data"]["user"])

    @reauth_on_fail
    def get_connections(self) -> list[Connection]:
        """Get all connections (patients) the user can access.
        
        Returns:
            A list of Connection objects.
            
        Raises:
            requests.HTTPError: If the API request fails.
        """
        if (self.missing_auth_header):
            self.authenticate()

        r = self.client.get(
            f"{self.base_url}/llu/connections",
        )
        r.raise_for_status()
        return Connection.from_list(r.json()["data"])
    
    @reauth_on_fail
    def get_graph(self, patient_id: UUID) -> list[GlucoseMeasurement]:
        """Get glucose measurement data for a specific patient.
        
        Args:
            patient_id: The UUID of the patient to retrieve data for.
            
        Returns:
            A list of GlucoseMeasurement objects for the patient.
            
        Raises:
            requests.HTTPError: If the API request fails.
        """
        if (self.missing_auth_header):
            self.authenticate()

        r = self.client.get(
            f"{self.base_url}/llu/connections/{patient_id}/graph",
        )
        r.raise_for_status()
        return [GlucoseMeasurement.from_dict(measurement) for measurement in r.json()["data"]["graphData"]]
