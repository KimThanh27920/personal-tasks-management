from django.urls import path, include
from .views import *

urlpatterns = [
    path('tasks/',TaskAPI.as_view(),name='tasks'),
    path('tasks/<int:task_id>', TaskDetailAPI.as_view(),name='detail-task')
]