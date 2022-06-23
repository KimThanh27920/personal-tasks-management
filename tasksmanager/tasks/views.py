from django.forms import ValidationError
from django.shortcuts import render

from rest_framework import generics, filters
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .serializers import *
from workspaces.mypermissions import IsOwnerWorkspace
# Create your views here.

class PriorityAPI(generics.ListCreateAPIView):
    serializer_class = PrioritySerializer
    queryset = Priority.objects.all()
    permission_classes =[IsAdminUser]

class PriorityUpdateAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PrioritySerializer
    queryset = Priority.objects.all()
    lookup_url_kwarg = 'priority_id'
    permission_classes =[IsAdminUser]
#status
class StatusAPI( generics.ListCreateAPIView):
    serializer_class = StatusSerializer
    queryset = Status.objects.all()
    #lookup_url_kwarg = 'status_id'
    permission_classes = [IsAdminUser]

class StatusUpdateAPI( generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StatusSerializer
    queryset = Status.objects.all()
    lookup_url_kwarg = 'status_id'
    permission_classes = [IsAdminUser]
#tasks
class TaskAPI(generics.ListCreateAPIView):
    serializer_class =  TaskSerializer
    
    #queryset = Task.objects.all()

    permission_classes = [IsAuthenticated, IsOwnerWorkspace]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['status__status','priority__priority']
    filterset_fields = ['status']
    lookup_url_kwarg = 'workspace_id'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskReadSerializer
        return TaskSerializer
    
    def get_queryset(self):
        self.queryset = Task.objects.filter(workspace=self.kwargs['workspace_id'])
        return super().get_queryset()

    def perform_create(self, serializer):
        try:
            workspace = Workspace.objects.get(id=self.kwargs['workspace_id'])
            serializer.save(workspace=workspace)
        except:
            ValidationError('Workspace do not exists')
        return super().perform_create(serializer)
    
    
class TaskDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerWorkspace,IsAuthenticated]
    
    queryset = Task.objects.all()
    lookup_url_kwarg = 'task_id'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskReadSerializer
        return TaskSerializer

