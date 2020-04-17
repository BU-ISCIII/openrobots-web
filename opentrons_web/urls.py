from django.contrib import admin
from django.urls import include ,path
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('',include ('opentrons.urls')),
    path('background', LoginView.as_view(template_name='opentrons/background.html'), name="background"),
    path('bu-isciii', LoginView.as_view(template_name='opentrons/bu_isciii.html'), name="about-us"),
    path('contact', LoginView.as_view(template_name='opentrons/contact.html'), name="contact"),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('utils/',include('django_utils.urls')),
    
]
