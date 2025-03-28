# OLX searching/autosuggest/filtering logic

# pink_olx_logic.py

from olx_api.authentication import OLXAuth
from olx_api.search import Search


def create_search_api(use_login, username, password, token_text, device_name="pink_olx_app"):
    """
    Creates and returns a Search instance.
    If 'use_login' is True and username/password are provided, we authenticate.
    Otherwise, we use the token_text if available, or no token at all.
    """
    if use_login:
        if username and password:
            try:
                auth = OLXAuth(username=username, password=password, device_name=device_name)
                logged_token = auth.login()
                return Search(token=logged_token)
            except Exception as e:
                print(f"[Login Error] {e}")
                return Search(token=None)
        else:
            # fallback to token
            return Search(token=token_text or None)
    else:
        # Not using login
        if token_text:
            return Search(token=token_text)
        else:
            return Search(token=None)


def autosuggest_olx(search_api, query):
    """
    Calls the /autosuggest endpoint. Returns a dict with 'autocomplete', 'categories', etc.
    """
    if not search_api:
        return {}

    try:
        data = search_api.autosuggest(query)
        return data
    except Exception as e:
        print(f"[Autosuggest Error] {e}")
        return {}


def search_all_listings(search_api, query, per_page, max_pages):
    """
    Calls the custom method 'search_all_listings' from your 'search.py' to get multiple pages.
    """
    if not search_api:
        return []

    try:
        results = search_api.search_all_listings(
            q=query,
            per_page=per_page,
            max_pages=max_pages
        )
        return results
    except Exception as e:
        print(f"[Search Error] {e}")
        return []


def filter_listings_by_price_condition(listings, min_price, max_price, condition):
    """
    Filters listings by optional min_price, max_price, and condition ('new', 'used', or 'All').
    Returns filtered list.
    """
    # Price Filter
    filtered = []
    for item in listings:
        try:
            p = float(item.get("price", 0) or 0)
        except ValueError:
            p = 0

        if min_price is not None and p < min_price:
            continue
        if max_price is not None and p > max_price:
            continue
        filtered.append(item)

    # Condition Filter
    if condition != "All":
        filtered = [f for f in filtered if f.get("state", "").lower() == condition.lower()]

    return filtered


def sort_listings_by_price(listings, sort_order):
    """
    Sorts by price ascending ('Ascending') or descending ('Descending'). 'None' -> no sort.
    Returns a *new* sorted list.
    """
    if sort_order == "None":
        return listings

    reverse_sort = (sort_order == "Descending")
    def get_price(item):
        try:
            return float(item.get("price", 0) or 0)
        except ValueError:
            return 0

    return sorted(listings, key=get_price, reverse=reverse_sort)
