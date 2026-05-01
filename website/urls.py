from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('events/', views.event_list, name='event_list'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
]