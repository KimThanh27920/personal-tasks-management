
from django.db import models
from workspaces.models import Workspace
# # Create your models here.
class Status(models.Model):
    status = models.CharField(unique=True, max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'status'
    
    def __str__(self):
        return self.status

class Priority(models.Model):
    priority = models.CharField(unique=True, max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'priority'
    
    def __str__(self):
        return self.priority


class Task(models.Model):
    task_name = models.CharField(max_length=255, null= None)
    workspace = models.ForeignKey(Workspace,on_delete=models.CASCADE, null=None)
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE, null=None)
    status = models.ForeignKey(Status, on_delete=models.CASCADE,default= 1 )
    description = models.TextField(null=True)
    due = models.DateField(null= None)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tasks'

    def __str__(self):
        return self.task_name
