
import json
from channels.generic.websocket import WebsocketConsumer


class ActionConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        print(text_data)
        message = {
            'message': text_data,
            'and this': text_data
        }
        self.send(text_data=json.dumps(message))
        self.send(text_data=json.dumps(message))
