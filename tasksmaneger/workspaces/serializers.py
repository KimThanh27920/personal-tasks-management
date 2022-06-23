from rest_framework import serializers
from .models import Workspace, Images_Workspace

class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = '__all__'

        read_only_fields = ['id','user']

class WorkspaceUpdateSerializer(serializers.Serializer):
    class Meta:
        model = Workspace
        fields = '__all__'

        read_only_fields = ['id','user']



class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images_Workspace
        fields = '__all__'

