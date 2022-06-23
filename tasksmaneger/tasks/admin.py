from django.contrib import admin
from .models import Status, Priority, Task
# Register your models here.
admin.site.register(Status)
admin.site.register(Priority)
admin.site.register(Task)