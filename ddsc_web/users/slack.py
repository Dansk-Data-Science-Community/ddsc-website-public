import logging
from typing import Optional

import requests


logger = logging.getLogger(__name__)


def post_greeting(webhook_url: str, channel: str, *, full_name: str, email: str) -> bool:
    payload = {
        "channel": channel,
        "text": f"👋 Please welcome {full_name or email} to DDSC!",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*New member onboarding*\n• Name: {full_name or 'N/A'}\n• Email: {email}",
                },
            }
        ],
    }

    try:
        response = requests.post(webhook_url, json=payload, timeout=5)
        response.raise_for_status()
        return True
    except requests.RequestException as exc:
        logger.warning("slack_webhook_failed", extra={"error": str(exc)})
        return False
