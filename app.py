import json

from flask import Flask, request

import tg

app = Flask(__name__)
http = bot_init()


@app.route("/webhook", methods=["POST"])
def webhook():
    """Handle POST requests"""
    data = request.get_json()
    if not data:
        # Don't say nothin'. This can't be Telegram
        return 200

    print(data)
    if (message := data.get("message")) :
        chat_id = message["chat"]["id"]
        msg_id = message["id"]
        if (text := message["text"]).lower() == "ping":
            r = tg.send_message(http, chat_id, "PONG!!", reply_to=msg_id)

    return 200
