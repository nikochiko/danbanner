import json
import logging
import os

import urllib3
from dotenv import load_dotenv


load_dotenv()
logger = logging.getLogger("DANBANNER")

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
TELEGRAM_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
TELEGRAM_BASE_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


def bot_init():
    http = urllib3.PoolManager()

    delete_webhook_url = f"{TELEGRAM_BASE_API_URL}/deleteWebhook"
    set_webhook_url = f"{TELEGRAM_BASE_API_URL}/setWebhook"
    set_webhook_data = json.dumps(
        {"url": WEBHOOK_URL, "allowed_updates": ["message"]}
    )

    # First remove all webhook integration
    http.request("GET", delete_webhook_url)

    # Then add it again
    response = http.request(
        "POST",
        set_webhook_url,
        body=set_webhook_data,
        headers={"Content-Type": "application/json"},
    )

    if response.status_code == 200:
        logger.info("Webhook successfully reset")
    else:
        response = json.loads(response.data.decode("utf-8"))
        raise Exception("Can't reset webhook integration: " + str(response))

    return http


def send_message(
    http, chat_id, text, parse_mode="MarkdownV2", reply_to=None, **kwargs
):

    send_message_url = f"{TELEGRAM_BASE_API_URL}/sendMessage"
    send_message_data = json.dumps(
        {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "reply_to_message_id": reply_to,
            **kwargs,
        }
    )

    response = http.request(
        "POST",
        send_message_url,
        body=send_message_data,
        headers={"Content-Type": "application/json"},
    )

    feedback = json.loads(response.data.decode("utf-8"))
    if feedback.get("ok"):
        logger.info("Successfully sent message")
    else:
        raise Exception("Unable to send message: " + feedback["description"])
