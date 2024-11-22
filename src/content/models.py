import os
from django.db import models
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
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

    def get_breadcrumbs(self):
        breadcrumbs = []
        folder = self
        while folder:
            breadcrumbs.insert(0, folder)
            folder = folder.parent_folder
        return breadcrumbs

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
    thumbnail = models.CharField(max_length=255, null=True, blank=True)
    duration = models.CharField(max_length=50, null=True, blank=True)
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
        if self.file_type == 'image' or self.file_type == 'video':
            return self.file.url
        else:
            return static('icons/video-thumbnail.png')

    def get_duration(self):
        """
        Extracts the duration of a video file using Hachoir.
        If the file is not a video, returns " - ".
        """
        if self.file_type == 'video':
            try:
                parser = createParser(self.file.path)
                if parser:
                    metadata = extractMetadata(parser)
                    if metadata and metadata.has("duration"):
                        duration_in_seconds = metadata.get("duration").seconds
                        minutes, seconds = divmod(duration_in_seconds, 60)
                        return f"{minutes}m {seconds}s"
                    else:
                        return "N/A"
                else:
                    return "N/A"
            except Exception as e:
                print(f"Error extracting video duration: {e}")
                return "N/A"
        return " -"

    class Meta:
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        self.set_file_type()
        self.thumbnail = self.get_thumbnail_url()
        self.duration = self.get_duration()
        super().save(*args, **kwargs)
