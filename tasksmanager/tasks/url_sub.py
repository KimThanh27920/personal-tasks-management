from tkinter import N
from django.urls import path
from .views import *

urlpatterns = [
    path('status/', StatusAPI.as_view(),name='list-status'),
    path('status/<status_id>', StatusUpdateAPI.as_view(),name='update-status'),
    path('priority/', PriorityAPI.as_view(),name='list-priority'),
    path('priority/<priority_id>', PriorityUpdateAPI.as_view(),name='update-priority'),
]