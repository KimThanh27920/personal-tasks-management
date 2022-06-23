# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from .mypermissions import IsOwnerOrReadOnly, IsOwner, IsOwnerWorkspace

from rest_framework import status

from .serializers import WorkspaceSerializer, ImageSerializer
from .models import Workspace,Images_Workspace

class WorkspaceAPIView(generics.ListCreateAPIView):
    permission_classes =[IsAuthenticated]

    serializer_class = WorkspaceSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:

            return Workspace.objects.all()
        return Workspace.objects.filter(user = self.request.user)
   
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)

class WorkspaceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkspaceSerializer
    queryset = Workspace.objects.all()
    permission_classes =[IsOwnerOrReadOnly]
    lookup_field = 'id'
    lookup_url_kwarg = 'workspace_id'

class ImageAPIView(generics.CreateAPIView):
    permission_classes =[IsOwnerOrReadOnly]
    serializer_class  = ImageSerializer
    queryset = Images_Workspace.objects.all()
    lookup_url_kwarg = 'workspace_id'

    def create(self, request, *args, **kwargs):
        lookup_url_kwarg = self.lookup_url_kwarg
        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )
        workspace_id = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        request.data['workspace'] = workspace_id.get('pk')
        return super().create(request, *args, **kwargs)

class ImageUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes =[IsOwnerWorkspace]
    serializer_class  = ImageSerializer
    queryset = Images_Workspace.objects.all()
    lookup_url_kwarg = 'workspace_id'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)