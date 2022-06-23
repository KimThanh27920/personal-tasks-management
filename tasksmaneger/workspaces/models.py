
from django.db import models
from users.models import CustomUser
# Create your models here.
class Workspace(models.Model):
    tilte = models.CharField(max_length=255,null= None)
    description = models.TextField() 
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'workspaces'

    def __str__(self):
        return self.tilte

class Images_Workspace(models.Model):
    workspace = models.OneToOneField(Workspace,primary_key=True, on_delete= models.CASCADE)
    url = models.ImageField(upload_to='workspaces_img/')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'image_workspace'
    
    def __str__(self):
        return str(self.workspace)



