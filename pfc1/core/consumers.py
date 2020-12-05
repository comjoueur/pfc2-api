
import json
from channels.generic.websocket import WebsocketConsumer
from pfc1.core.models import Client, Touch
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from pfc1 import utils


class ActionConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = None

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = None

    def connect(self):
        self.client = Client.objects.create(channel_ws=self.channel_name,
                                            token=Client.generate_valid_client_token())
        self.accept()

    def disconnect(self, code):
        self.client.delete()

    def receive(self, text_data=None, bytes_data=None):
        data = text_data.split(':')
        if data[0] == 'token':
            self.client = Client.objects.filter(token=data[1]).first()

        if not self.client:
            return

        if data[0] == 'action':
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.send)(self.client.channel_ws, {
                'type': 'send.message',
                'message': json.dumps({'key': utils.keyCode[data[1]]})
            })

        elif data[0] == 'touch':
            Touch.objects.create(
                button=data[3] or None,
                position_x=int(data[1]),
                position_y=int(data[2]),
                client=self.client
            )
            self.client.save_centers()
            self.send('centers:{}:{}:{}:{}'.format(self.client.center_directionals[0],
                                                   self.client.center_directionals[1],
                                                   self.client.center_directionals[2],
                                                   self.client.center_directionals[3]))
