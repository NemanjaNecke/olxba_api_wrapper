## OLX API Python Library
>A lightweight Python wrapper for interacting with the OLX API. This library simplifies making HTTP requests to the various OLX endpoints, including authentication, listings, categories, locations, sponsored listings, and user-related queries. It’s designed to be easy to use, extendable, and follows best practices for logging and error handling.

## Features
**Authentication:**
>Easily authenticate and obtain a Bearer token with your OLX credentials.

**Listings:**
>Create, update, publish, refresh, and manage images for listings.

**Categories:**
>Retrieve all categories, children categories, attributes, brands, models, and perform searches or suggestions.

**Locations:**
>Fetch data for cities, countries, states, and canton-specific cities.

**Sponsored Listings:**
vSponsor listings, retrieve sponsorship pricing, set discounts, and finish discounts.

**Users:**
>Retrieve active, finished, inactive, expired, and hidden listings for a given user.

## Installation
>Clone the repository and install it locally
```
git clone https://github.com/NemanjaNecke/olxba_api_py_wrapper.git
cd olx_api
pip install -r requirements.txt
```

**Alternatively, you can use it as a local package by installing it in editable mode:**
```
pip install -e .
```

## Usage
>Below are some examples that show how to use different parts of the library.

**Authentication**
Authenticate with the OLX API using your credentials:
```
from olx_api.authentication import OLXAuth

# Replace with your actual credentials.
auth = OLXAuth(username="your_email@olx.ba", password="your_password", device_name="integration")
token = auth.login()

print("Token:", token)
```

>For other examples see integration_test
