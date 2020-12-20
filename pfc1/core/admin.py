
from django.contrib import admin
from pfc1.core.models import Client, Touch, Button


@admin.register(Client)
class ClientModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Button)
class ButtonModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Touch)
class TouchModelAdmin(admin.ModelAdmin):
    pass
