from typing import Optional
import requests
from LibreView.models import User, Connection
from hashlib import sha256


def reauth_on_fail(func):
    def wrapper(*args):
        try:
            return func(*args)
        except requests.HTTPError as e:
            if e.response.status_code == 401:
                api: API = args[0]
                api.authenticate()
                return func(*args)
            raise e
    return wrapper


class API:
    def __init__(self, username: str, password: str, region: Optional[str] = None):
        self.base_url = "https://api.libreview.io"
        if region:
            self.base_url = f"https://api-{region}.libreview.io"
        self.client = requests.session()
        self.product = "llu.android"
        self.version = "4.12.0"
        self.username = username
        self.password = password
        self.client.headers["product"] = self.product
        self.client.headers["version"] = self.version

    @property
    def missing_auth_header(self):
        return self.client.headers.get("Authorization") is None

    def authenticate(self):
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

    def set_token(self, token):
        self.client.headers["Authorization"] = f"Bearer {token}"

    def accept_terms(self, token):
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
        if (self.missing_auth_header):
            self.authenticate()

        r = self.client.get(
            f"{self.base_url}/user",
        )
        r.raise_for_status()
        return User.from_dict(r.json()["data"]["user"])

    @reauth_on_fail
    def get_connections(self) -> list[Connection]:
        if (self.missing_auth_header):
            self.authenticate()

        r = self.client.get(
            f"{self.base_url}/llu/connections",
        )
        r.raise_for_status()
        return Connection.from_list(r.json()["data"])
