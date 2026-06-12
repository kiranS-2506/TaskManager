from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.TasksListApiView.as_view(), name='task-list-create'),
    path('tasks-detail/<uuid:id>/', views.TaskDetailApiView.as_view(), name='task-detail'),
]