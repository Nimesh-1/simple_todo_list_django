from django.urls import path
from .views import register_page, task_create, task_list, task_detail, task_update, task_delete, custom_login
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/',custom_login, name='login'),
    path('logout/',LogoutView.as_view(next_page='login'), name='logout'),
    path('register/',register_page, name='register'),

    path('', task_list, name='tasks'),
    path('task/<int:pk>/', task_detail, name='task'),
    path('task-create/', task_create, name='task-create'),
    path('task-update/<int:pk>/', task_update, name='task-update'),
    path('task-delete/<int:pk>/', task_delete, name='task-delete'),
    
]