from django.urls import path
from main.views import home, contacts
from main.apps import MainConfig

app_name = MainConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('contacts/', contacts, name='contacts'),
]
