from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('event/<int:event_id>/status/<str:status>/', views.update_event_status, name='update_event_status'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]