# urls.py (main app urls)
from django.urls import path
from . import views

urlpatterns = [
    # Home and Authentication
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('setup-profile/<int:user_id>/', views.setup_profile_view, name='setup_profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Tasks
    path('tasks/', views.task_list_view, name='task_list'),
    path('tasks/create/', views.task_create_view, name='task_create'),
    path('tasks/<int:task_id>/', views.task_detail_view, name='task_detail'),
    path('tasks/<int:task_id>/update/', views.task_update_view, name='task_update'),
    path('tasks/<int:task_id>/delete/', views.task_delete_view, name='task_delete'),
    path('tasks/<int:task_id>/toggle/', views.toggle_task_status, name='task_toggle'),
    
    # Profile
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.profile_update_view, name='profile_update'),
    path('change-password/', views.change_password_view, name='change_password'),
]

