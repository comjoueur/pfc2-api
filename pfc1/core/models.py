
from django.db import models
import string
import secrets


class Client(models.Model):
    TOKEN_SIZE = 10

    channel_ws = models.CharField(max_length=256)
    token = models.CharField(max_length=TOKEN_SIZE, unique=True)

    @classmethod
    def generate_valid_client_token(cls):
        alphabet = string.digits
        valid_token = False
        token = None
        while not valid_token:
            token = ''.join(secrets.choice(alphabet) for _ in range(cls.TOKEN_SIZE))
            valid_token = not cls.objects.filter(token=token).exists()
        return token
