
from django.db import models
import string
import secrets
from sklearn.cluster import KMeans
import numpy as np


class Client(models.Model):
    TOKEN_SIZE = 8
    NUM_CLUSTERS = 2
    CORRECT_WEIGHT = 3
    INCORRECT_WEIGHT = 1

    channel_ws = models.CharField(max_length=256)
    token = models.CharField(max_length=TOKEN_SIZE, unique=True)
    center_x = models.IntegerField(default=0)
    center_y = models.IntegerField(default=0)
    options_x = models.IntegerField(default=0)
    options_y = models.IntegerField(default=0)

    @property
    def center_directionals(self):
        return self.center_x, self.center_y

    @center_directionals.setter
    def center_directionals(self, new_center):
        self.center_x = new_center[0]
        self.center_y = new_center[1]

    @property
    def center_options(self):
        return self.options_x, self.options_y

    @center_options.setter
    def center_options(self, new_options):
        self.options_x = new_options[0]
        self.options_y = new_options[1]

    @classmethod
    def generate_valid_client_token(cls):
        alphabet = string.digits
        valid_token = False
        token = None
        while not valid_token:
            token = ''.join(secrets.choice(alphabet) for _ in range(cls.TOKEN_SIZE))
            valid_token = not cls.objects.filter(token=token).exists()
        return token

    def get_centroids(self, weighted=False):
        touches = self.get_touches_positions(weighted=weighted)
        if len(touches) < self.NUM_CLUSTERS:
            return None
        array_touches = np.array(touches)
        kmeans = KMeans(n_clusters=self.NUM_CLUSTERS, init='k-means++', random_state=0).fit(array_touches)
        return kmeans.cluster_centers_

    def get_touches_positions(self, weighted=False):
        if weighted:
            touches = []
            for touch in self.touches.all():
                touches += [touch.position] * (self.CORRECT_WEIGHT if touch.button else self.INCORRECT_WEIGHT)
            return touches
        return [touch.position for touch in self.touches.all()]

    def save_centers(self):
        centers = self.get_centroids()
        if centers is not None:
            self.center_directionals = centers[0] if centers[0][0] < centers[1][0] else centers[1]
            self.center_options = centers[0] if centers[1][0] < centers[0][0] else centers[1]


class Touch(models.Model):
    BUTTON_LEFT = 'left'
    BUTTON_UP = 'up'
    BUTTON_RIGHT = 'right'
    BUTTON_DOWN = 'down'
    BUTTON_PAUSE = 'pause'
    BUTTON_START = 'start'
    KIND_BUTTON_CHOICES = [
        (BUTTON_LEFT, 'Left Button'),
        (BUTTON_RIGHT, 'Right Button'),
        (BUTTON_DOWN, 'Down Button'),
        (BUTTON_UP, 'Up Button'),
        (BUTTON_START, 'Start Button'),
        (BUTTON_PAUSE, 'Pause Button'),
    ]

    button = models.CharField(null=True, blank=True, max_length=32, choices=KIND_BUTTON_CHOICES)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='touches')
    position_x = models.IntegerField(default=0)
    position_y = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    @property
    def position(self):
        return self.position_x, self.position_y

    @position.setter
    def position(self, new_position):
        self.position_x = new_position[0]
        self.position_y = new_position[1]

    def __str__(self):
        return '{}, {}, {}'.format(self.position_x, self.position_y, self.button)
