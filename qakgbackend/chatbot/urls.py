# chatbot/urls.py
from django.urls import path
from .views import  get_question

urlpatterns = [

    path('get_question/', get_question, name='get_question'),
]