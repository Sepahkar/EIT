import os

from django.apps import AppConfig


class CartableConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    if "Portal" in str(os.getcwd()):
        name = 'Cartable'
    else:
        name = 'Portal.Cartable'
