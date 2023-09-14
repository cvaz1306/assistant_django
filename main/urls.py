from django.urls import path
from . import views
urlpatterns = [
    path('',views.main),
    path('mess',views.mess),
    path('contact', views.contact),
]