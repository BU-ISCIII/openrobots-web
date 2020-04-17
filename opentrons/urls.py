from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name = 'index'),
    path('requestFile', views.request_file, name = 'request_file')
	]
