from django.urls import path, re_path, include

from upload import views

urlpatterns = [
    re_path(r'^hello$', views.hello),
    re_path(r'^uploadFile$', views.uploadFile),
    re_path(r'^getFileList$', views.getFileList),
]