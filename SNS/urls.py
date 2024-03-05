from django.urls import path
from . import views

app_name = 'SNS'

urlpatterns = [
    path('home/', views.home, name='home'), 
]
