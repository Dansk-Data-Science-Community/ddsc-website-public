import requests
import time

from typing import Callable
from functools import partial


def get_newsletter_subscriber_id(
    email: str,
    api_url: str,
    api_key: str,
) -> int | None:
    url = f"{get_subscribers_endpoint(api_url)}/{email}"
    headers = get_auth_header(api_key)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        subscriber_data = response.json()
        return subscriber_data["data"].get("id")
    elif response.status_code == 404:
        return None
    else:
        response.raise_for_status()


def forget_newsletter_subscriber(
    subscriber_id: int,
    api_url: str,
    api_key: str,
) -> bool:
    """GDPR compliant endpoint to delete a subscriber entirely after 30 days."""
    url = url = f"{get_subscribers_endpoint(api_url)}/{subscriber_id}/forget"
    headers = get_auth_header(api_key)
    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False
    else:
        response.raise_for_status()


def get_subscribers_list(
    api_url: str,
    api_key: str,
    limit=25,
) -> list[dict[str, str]]:
    url = get_subscribers_endpoint(api_url)
    params = {"filter[status]": "active", "limit": limit}
    headers = get_auth_header(api_key)

    subscribers = []
    cursor = None

    while True:
        if cursor:
            params["cursor"] = cursor

        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            response.raise_for_status()

        data = response.json()
        for subscriber in data["data"]:
            subscribers.append({"email": subscriber["email"], "id": subscriber["id"]})

        cursor = data.get("meta", {}).get("next_cursor")
        if not cursor:
            break

    return subscribers


def subscribe_to_newsletter(
    email: str,
    name: str,
    api_url: str,
    api_key: str,
) -> requests.Response:
    url = get_subscribers_endpoint(api_url)
    headers = get_auth_header(api_key)
    payload = get_subscribe_payload(email, name)
    lazy_request = partial(requests.post, url=url, json=payload, headers=headers)
    response = lazy_request()
    if response.status_code == 429:
        response = retry_delayed(lazy_request, response)

    return response


def get_subscribers_endpoint(api_url: str) -> str:
    return f"{api_url}/subscribers"


def get_subscribe_payload(email: str, name: str) -> dict[str, str | int]:
    return {
        "email": email,
        "name": name,
        "resubscribe": 1,
    }


def get_auth_header(api_key: str) -> dict[str, str]:
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }


def retry_delayed(
    lazy_request: Callable,
    ratelimit_response: requests.Response,
) -> requests.Response:
    retry_after = int(ratelimit_response.headers.get("Retry-After", 1))
    time.sleep(retry_after)
    return lazy_request()
