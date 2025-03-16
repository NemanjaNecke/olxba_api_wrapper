# olx_api/authentication.py
from olx_api.base import OLXBase
import requests


class OLXAuth(OLXBase):
    """
    A simple wrapper for authenticating with the OLX API.

    Usage:
        auth = OLXAuth(username="test@olx.ba", password="password", device_name="integration")
        token = auth.login()
        headers = auth.get_authenticated_headers()
    """

    def __init__(self, username, password, device_name="integration"):
        """
        Initialize the OLXAuth instance with credentials.

        :param username: The username or email for login.
        :param password: The password.
        :param device_name: A string identifier for the device (default: "integration").
        """
        super().__init__()  # No token initially
        self.username = username
        self.password = password
        self.device_name = device_name
        self.token = None
        self.user = None

    def login(self):
        """
        Authenticates with the OLX API using the /auth/login endpoint.

        Sends a POST request with a JSON payload including:
            - username (or email)
            - password
            - device_name

        Example cURL:
            curl https://api.olx.ba/auth/login \
                -d username="test@olx.ba" \
                -d password="password" \
                -d device_name="integration"

        On success, stores and returns the token from the API response.

        :return: The authentication token as a string.
        :raises: HTTPError if the request fails.
        """
        url = f"{self.BASE_URL}/auth/login"
        payload = {
            "username": self.username,
            "password": self.password,
            "device_name": self.device_name,
        }
        headers = self._get_headers()
        headers["Accept"] = "application/json"
        response = requests.post(url, json=payload, headers=headers)
        data = self._handle_response(response)
        self.token = data.get("token")
        self.user = data.get("user")
        return self.token

    def get_authenticated_headers(self):
        """
        Returns a headers dictionary including the Bearer token for authenticated requests.

        :return: A dict with the 'Authorization' header.
        :raises: ValueError if no token is available.
        """
        if not self.token:
            raise ValueError("No token found. Please login first using the login() method.")
        return {"Authorization": f"Bearer {self.token}"}

    @staticmethod
    def get_headers_with_old_tokens(client_id, client_token):
        """
        Returns headers using the legacy authentication method,
        which requires OLX-CLIENT-ID and OLX-CLIENT-TOKEN headers.

        :param client_id: The client id provided by OLX.
        :param client_token: The client token provided by OLX.
        :return: A dict with legacy authentication headers.
        """
        return {
            "OLX-CLIENT-ID": client_id,
            "OLX-CLIENT-TOKEN": client_token
        }
