# olx_api/base.py

import logging
import requests


class OLXBase:
    BASE_URL = "https://api.olx.ba"
    USER_AGENT = "olx_api/0.1.0"

    def __init__(self, token=None):
        """
        Base initializer that accepts an optional token.

        :param token: Optional Bearer token for authentication.

        Example logging:
        if not self.logger.handlers:
            file_handler = logging.FileHandler("olx_api.log", encoding="utf-8")
            file_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        """
        self.token = token
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.addHandler(logging.NullHandler())

    def _get_headers(self, multipart=False):
        """
        Returns the common headers for authenticated requests.

        :param multipart: If True, skip setting Content-Type header (so requests can add the proper one).
        :return: A dictionary of HTTP headers.
        """
        headers = {
            "User-Agent": self.USER_AGENT
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        # Only set Content-Type if not sending multipart data
        if not multipart:
            headers["Content-Type"] = "application/json"
        return headers

    def _handle_response(self, response):
        """
        Common method to log, raise errors, and return JSON from a response.

        Logs the response status code and JSON content (or text if not JSON).

        :param response: The HTTP response object.
        :return: Parsed JSON from the response.
        :raises: HTTPError if the response status indicates an error.
        """
        self.logger.debug("Response Status Code: %s", response.status_code)
        try:
            json_response = response.json()
            self.logger.debug("Response JSON: %s", json_response)
        except Exception as e:
            self.logger.debug("Response is not valid JSON. Raw response: %s", response.text)
        response.raise_for_status()
        return response.json()
