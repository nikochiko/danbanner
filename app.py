import json

import falcon
import falcon.asgi

import tg


class Webhook:
    def __init__(self):
        self.http = tg.bot_init()    

    async def on_post(self, req, resp):
        """Handle POST requests"""
        if req.content_length:
            data = json.load(req.stream)
        else:
            # Don't say nothin'. This can't be Telegram
            resp.status = falcon.HTTP_200
            return
        
        print(data)
        if (message := data.get("message")):
            chat_id = message["chat"]["id"]
            msg_id = message["id"]
            if (text := message["text"]).lower() == "ping":
                r = tg.send_message(self.http, chat_id, "PONG!!", reply_to=msg_id)

        resp.status = falcon.HTTP_200


app = falcon.asgi.App()

webhook = Webhook()

app.add_route("/webhook", webhook)