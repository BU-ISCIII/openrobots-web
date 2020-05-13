from django.urls import path

from openrobots.api.views import *

app_name = 'openrobots'

urlpatterns = [
        path('', api_usage, name ='api_usage' ),
        path('createUsage', api_create_usage, name='api_create_usage'),

]
