from django.contrib import admin

# Register your models here.
from content.models import Folder,File

admin.site.register(Folder)
admin.site.register(File)

