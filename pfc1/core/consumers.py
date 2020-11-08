
import json
from channels.generic.websocket import WebsocketConsumer
from pfc1.core.models import Client
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from pfc1 import utils


class ActionConsumer(WebsocketConsumer):
    client = None

    def connect(self):
        self.client = Client.objects.create(channel_ws=self.channel_name,
                                            token=Client.generate_valid_client_token())
        self.accept()

    def disconnect(self, close_code):
        self.client.delete()

    def receive(self, text_data=None, bytes_data=None):
        if text_data == 'token':
            credentials = {
                'token': self.client.token,
            }
            self.send(text_data=json.dumps(credentials))

    def send_message(self, message):
        self.send(text_data=message['message'])


class ControllerConsumer(WebsocketConsumer):
    client = None

    def connect(self):
        self.accept()

    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        data = text_data.split(':')
        if data[0] == 'token':
            self.client = Client.objects.filter(token=data[1]).first()
        elif data[0] == 'action':
            action = {
                'key': utils.keyCode[utils.START_OPTION],
            }
            if self.client.pk:
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.send)(self.client.channel_ws, {
                    'type': 'send_message',
                    'message': json.dumps(action)
                })
