from django.urls import path, include
from .views import *

urlpatterns = [
    path('',WorkspaceAPIView.as_view(),name='list-workspace'),
    path('<int:workspace_id>/', WorkspaceDetailAPIView.as_view(),name='detail-workspace'),
    path('<int:workspace_id>/upload/', ImageAPIView.as_view(),name='upload-image-workspace'),
    path('<int:workspace_id>/update-image-workspace/', ImageUpdateAPIView.as_view(),name='update-image-workspace'),
]