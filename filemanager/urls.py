from django.urls import path
from . import views
urlpatterns=[
    path('', view=views.filemanager),
    path('upload', views.upload_file, name='upload_file'),
    path('files', views.files),
    path('get', views.getFile)
]