from olx_api.base import OLXBase
import requests
import math


class Search(OLXBase):
    """
    Search API Wrapper

    This class provides methods for interacting with the OLX search and autosuggest endpoints.
    The search endpoint is paginated and supports filtering by query, category, and additional URL
    parameters (e.g. sort_by, sort_order, has_price, available, shop_only, shipping, sponsored).

    Usage Examples:
        >>> search_api = Search(token="your_valid_token")
        >>> # Fetch a single page (default 20 results)
        >>> result = search_api.search_listings(
        ...     q="iphone",
        ...     category_id=1092,
        ...     page=1,
        ...     per_page=20,
        ...     extra_params={
        ...         "sort_by": "price",
        ...         "sort_order": "asc",
        ...         "has_price": 1,
        ...         "available": 1,
        ...         "shop_only": 1,
        ...         "shipping": 1,
        ...         "sponsored": 1,
        ...     }
        ... )
        >>> print(result)
        >>>
        >>> # Fetch all listings matching the query using additional parameters
        >>> all_results = search_api.search_all_listings(
        ...     q="iphone",
        ...     category_id=1092,
        ...     per_page=20,
        ...     extra_params={
        ...         "sort_by": "price",
        ...         "sort_order": "asc",
        ...         "has_price": 1,
        ...         "available": 1,
        ...         "shop_only": 1,
        ...         "shipping": 1,
        ...         "sponsored": 1,
        ...     }
        ... )
        >>> print("Total listings found:", len(all_results))
    """

    def search_listings(self, q, category_id=None, page=1, per_page=40, attr="", attr_encoded=1, extra_params=None):
        """
        Performs a search on the OLX API with the given parameters.

        Constructs a URL like:
            https://olx.ba/api/search?attr=&attr_encoded=1&category_id=1092&q=iphone&page=1&per_page=20

        Additional query parameters can be passed in via the extra_params dictionary.

        :param q: Search query string.
        :param category_id: (Optional) Category ID to filter the search.
        :param page: Page number (default is 1).
        :param per_page: Number of results per page (default is 40 - gives most consistent results).
        :param attr: Additional attribute parameter (default is empty string).
        :param attr_encoded: Flag for attribute encoding (default is 1).
        :param extra_params: (Optional) A dict of extra URL parameters (e.g. sort_by, sort_order, etc.).
        :return: Parsed JSON response from the API.
        """
        url = f"{self.BASE_URL}/search"
        params = {
            "q": q,
            "page": page,
            "per_page": per_page,
            "attr": attr,
            "attr_encoded": attr_encoded,
        }
        if category_id is not None:
            params["category_id"] = category_id

        if extra_params:
            params.update(extra_params)

        response = requests.get(url, headers=self._get_headers(), params=params)
        return self._handle_response(response)

    def search_all_listings(self, q, category_id=None, per_page=40, attr="", attr_encoded=1, extra_params=None,
                            max_pages=None):
        """
        Retrieves all listings matching the search query by iterating through pages.

        First, a request (using the provided per_page and extra_params) is made to determine the total
        number of listings from meta information. The number of pages is determined using meta["last_page"]
        (if available) or calculated as total/per_page. Optionally, a maximum number of pages (max_pages) can
        be specified. If an error occurs on any page (e.g. a 429 or 500 error), the method prints the error
        and returns the aggregated listings so far.

        :param q: Search query string.
        :param category_id: (Optional) Category ID to filter the search.
        :param per_page: Number of results per page (default is 40 - gives most consistent results).
        :param attr: Additional attribute parameter.
        :param attr_encoded: Flag for attribute encoding.
        :param extra_params: (Optional) A dict of extra URL parameters.
        :param max_pages: (Optional) Maximum number of pages to fetch.
        :return: A flat list containing all listing dictionaries that match the query.
        """
        initial = self.search_listings(q, category_id, page=1, per_page=per_page, attr=attr, attr_encoded=attr_encoded,
                                       extra_params=extra_params)
        meta = initial.get("meta", {})
        total = meta.get("total", 0)
        listings = []

        if total == 0:
            return listings

        pages_needed = meta.get("last_page", math.ceil(total / per_page))
        if max_pages is not None:
            pages_needed = min(pages_needed, max_pages)

        print(f"Total listings (meta): {total}. Fetching in {pages_needed} page(s) with {per_page} per request.")

        for page in range(1, pages_needed + 1):
            try:
                response = self.search_listings(q, category_id, page=page, per_page=per_page, attr=attr,
                                                attr_encoded=attr_encoded, extra_params=extra_params)
            except Exception as e:
                print(f"Encountered error on page {page}: {e}. Returning aggregated listings so far.")
                break

            data = response.get("data", [])
            listings.extend(data)
            print(f"Fetched page {page}/{pages_needed}: {len(data)} listings.")

            if len(data) < per_page:
                print("Received fewer items than requested; assuming end of results.")
                break

        return listings

    def autosuggest(self, q, extra_params=None):
        """
        Retrieves autosuggest data for the given query.

        Request URL:
            https://olx.ba/api/autosuggest?q=<q>&... (extra params can be added)

        Response format example:
        {
            "data": {
                "autocomplete": ["politikin zabavnik", "politikin", "denis politikin"],
                "categories": [
                    {"id": 434, "name": "Stripovi", "count": 35, "parent_name": "Literatura"},
                    ...
                ],
                "users": [],
                "suggestions": []
            }
        }

        :param q: The search query.
        :param extra_params: (Optional) Additional query parameters.
        :return: A dictionary containing autosuggest data.
        """
        url = "https://olx.ba/api/autosuggest"
        params = {"q": q}
        if extra_params:
            params.update(extra_params)
        response = requests.get(url, headers=self._get_headers(), params=params)
        data = self._handle_response(response)
        return data.get("data", {})
