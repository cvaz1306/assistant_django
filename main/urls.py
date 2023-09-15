from django.urls import path
from . import views
from transformers import T5ForConditionalGeneration, T5Tokenizer
urlpatterns = [
    path('',views.main),
    path('mess',views.mess),
    path('contact', views.contact),
]