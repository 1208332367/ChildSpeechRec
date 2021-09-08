from django.urls import path, re_path, include

from recognize import views

urlpatterns = [
    re_path(r'^hello$', views.hello),
    re_path(r'^getInfo$', views.getInfo),
    re_path(r'^getHumanPart$', views.getHumanPart),
    re_path(r'^getRecognize$', views.getRecognize),
    re_path(r'^getAllJudge$', views.getAllJudge), 
    re_path(r'^modifyAnswer$', views.modifyAnswer),
    re_path(r'^clearCache$', views.clearCache),
    re_path(r'^getRedisCache$', views.getRedisCache),
]