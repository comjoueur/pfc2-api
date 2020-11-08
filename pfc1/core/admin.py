
from django.contrib import admin
from pfc1.core.models import Client


@admin.register(Client)
class ClientModelAdmin(admin.ModelAdmin):
    pass
