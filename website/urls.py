from django.urls import path
from . import views

urlpatterns = [

    # path('events/', views.event_list, name='event_list'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('', views.home, name='home'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('event/<int:event_id>/status/<str:status>/', views.update_event_status, name='update_event_status'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('user-events/', views.user_events, name='user_events'),
<<<<<<< HEAD
    path('events/', views.approved_events, name='event_list')
=======
    path('admin-dashboard/delete/<int:event_id>/', views.admin_delete_event, name='admin_delete_event'),
>>>>>>> 1ebf27ac182a8dc0a34adc5f183a670b1254de71
]