# olx_api/categories.py
from olx_api.base import OLXBase
import requests


class Categories(OLXBase):
    """
    Categories API Wrapper

    This class provides methods for interacting with the OLX API's category endpoints.
    It inherits from OLXBase, which sets up the base URL, user-agent, token, and common
    request header functionality.

    Usage Example:
        >>> categories = Categories(token="your_valid_token")
        >>> all_categories = categories.get_all_categories()
        >>> children = categories.get_children_categories(category_id=2)
        >>> category_details = categories.get_category(category_id=23)
        >>> attributes = categories.get_category_attributes(category_id=3)
        >>> brands = categories.get_category_brands(category_id=3)
        >>> models = categories.get_category_models(category_id=3, brand_id=7)
        >>> suggestions = categories.suggest_category(keyword="golf")
        >>> found = categories.find_category(name="felge")
    """

    def __init__(self, token):
        """
        Initializes the Categories API wrapper.

        :param token: A valid Bearer token for authentication.
        """
        super().__init__(token)

    def get_all_categories(self, include_children):
        """
        Retrieves all categories.

        GET /categories
        """
        if include_children:
            _include_children = 'true'
        else:
            _include_children = 'false'

        url = f"{self.BASE_URL}/categories?include_children={_include_children}"
        response = requests.get(url, headers=self._get_headers())
        data = self._handle_response(response)
        return data

    def get_children_categories(self, category_id):
        """
        Retrieves the children categories for a given category ID.

        GET /categories/:id
        """
        url = f"{self.BASE_URL}/categories/{category_id}"
        response = requests.get(url, headers=self._get_headers())
        data = self._handle_response(response)
        return data

    def get_category(self, category_id):
        """
        Retrieves a single category by its ID.

        GET /category/:id
        """
        url = f"{self.BASE_URL}/category/{category_id}"
        response = requests.get(url, headers=self._get_headers())
        data = self._handle_response(response)
        return data

    def get_category_attributes(self, category_id):
        """
        Retrieves attributes for a given category.

        GET /categories/:id/attributes
        """
        url = f"{self.BASE_URL}/categories/{category_id}/attributes"
        response = requests.get(url, headers=self._get_headers())
        data = self._handle_response(response)
        return data

    def get_category_brands(self, category_id):
        """
        Retrieves brands for a given category.

        GET /categories/:id/brands
        """
        url = f"{self.BASE_URL}/categories/{category_id}/brands"
        response = requests.get(url, headers=self._get_headers())
        data = self._handle_response(response)
        return data

    def get_category_models(self, category_id, brand_id):
        """
        Retrieves models for a given category and brand.

        GET /categories/:id/brands/:brand_id/models
        """
        url = f"{self.BASE_URL}/categories/{category_id}/brands/{brand_id}/models"
        response = requests.get(url, headers=self._get_headers())
        data = self._handle_response(response)
        return data

    def suggest_category(self, keyword):
        """
        Suggests categories based on a listing title keyword.

        GET /categories/suggest?keyword=...
        """
        url = f"{self.BASE_URL}/categories/suggest"
        params = {"keyword": keyword}
        response = requests.get(url, headers=self._get_headers(), params=params)
        data = self._handle_response(response)
        return data

    def find_category(self, name):
        """
        Finds categories by name.

        GET /categories/find?name=...
        """
        url = f"{self.BASE_URL}/categories/find"
        params = {"name": name}
        response = requests.get(url, headers=self._get_headers(), params=params)
        data = self._handle_response(response)
        return data
