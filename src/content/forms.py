from django import forms
from .models import File, Folder
import magic


class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name', 'parent_folder']


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'file', 'folder']

    def clean_file(self):
        file = self.cleaned_data.get('file')

        if not file:
            return file

        # Check file size
        file_size = file.size / (1024 * 1024)
        if file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            if file_size > 10:
                raise forms.ValidationError("Image files cannot exceed 10 MB.")
        elif file.name.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            if file_size > 50:
                raise forms.ValidationError("Video files cannot exceed 50 MB.")
        else:
            raise forms.ValidationError("Unsupported file type.")

        # Validate file MIME type
        mime = magic.Magic(mime=True)
        mime_type = mime.from_buffer(file.read(1024))  # Read the first 1024 bytes
        file.seek(0)  # Reset file pointer after reading

        if file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            if not mime_type.startswith('image/'):
                raise forms.ValidationError("The file is not a valid image.")
        elif file.name.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            if not mime_type.startswith('video/'):
                raise forms.ValidationError("The file is not a valid video.")

        return file


class RenameFolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name']

    name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter new folder name', 'class': 'form-control'}),
        label="New Folder Name"
    )


class RenameFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name']

    name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter new file name', 'class': 'form-control'}),
        label="New File Name"
    )