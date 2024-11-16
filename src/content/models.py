import os
from django.db import models
from user.models import User
from django.templatetags.static import static


class Folder(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='folders', on_delete=models.CASCADE)
    parent_folder = models.ForeignKey('self', related_name='subfolders', null=True, blank=True,
                                      on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    def get_thumbnail_url(self):
        return static('icons/folder-thumbnail.png')

    class Meta:
        unique_together = ('user', 'parent_folder', 'name')


def get_upload_path(instance, filename):
    user_id = instance.user.id
    folder_path = instance.folder.get_full_path()
    return os.path.join(f'uploads/user_{user_id}', folder_path, filename)


class File(models.Model):
    name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=10)
    file = models.FileField(upload_to='uploads/')
    user = models.ForeignKey(User, related_name='files', on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, related_name='files', null=True, blank=True, on_delete=models.CASCADE)
    size = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def set_file_type(self):
        if self.file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            self.file_type = 'image'
        elif self.file.name.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            self.file_type = 'video'
        else:
            raise ValueError("Unsupported file type")

    def get_thumbnail_url(self):
        if self.file_type == 'image':
            return self.file.url
        elif self.file_type == 'video':
            return self.file.url
        else:
            return static('icons/video-thumbnail.png')

    class Meta:
        ordering = ['created_at']

    def save(self, *args, **kwargs):  # Call set_file_type before saving the model
        self.set_file_type()
        super().save(*args, **kwargs)
