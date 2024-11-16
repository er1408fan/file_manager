from django import forms
from .models import File, Folder


# class FolderForm(forms.ModelForm):
#     class Meta:
#         model = Folder
#         fields = ['name', 'parent_folder']

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name', 'parent_folder']  # Include parent_folder if you want to set it directly in the form



class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'file', 'folder']

    def clean_file(self):
        file = self.cleaned_data.get('file')

        if not file:
            return file

        file_size = file.size / (1024 * 1024)
        if file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            if file_size > 10:
                raise forms.ValidationError("Image files cannot exceed 10 MB.")
        elif file.name.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            if file_size > 50:
                raise forms.ValidationError("Video files cannot exceed 50 MB.")
        else:
            raise forms.ValidationError("Unsupported file type.")

        return file


class RenameFolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name']  # Only allow renaming the 'name' field

    name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter new folder name', 'class': 'form-control'}),
        label="New Folder Name"
    )


class RenameFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name']  # Only allow renaming the 'name' field

    name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter new file name', 'class': 'form-control'}),
        label="New File Name"
    )