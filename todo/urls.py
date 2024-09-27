from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add-task/', views.add_task, name='add_task'),  # Add new task
    path('update-task/<str:pk>/', views.update_task, name='update_task'),
    path('delete-task/<str:pk>/', views.delete_task, name='delete_task'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),  # New URL pattern for task detail

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('profile/update/', views.profile_update, name='profile_update'),
]
