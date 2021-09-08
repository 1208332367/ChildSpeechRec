from django.conf.urls import url
from django.urls import include, re_path
from . import views

urlpatterns = [
    re_path(r'^upload/', include('upload.urls')),
    re_path(r'^recognize/', include('recognize.urls')),
]

