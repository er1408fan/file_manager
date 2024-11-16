from django.shortcuts import render
from django.urls import reverse_lazy
from .forms import FileForm, FolderForm, RenameFolderForm, RenameFileForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from content.models import Folder, File
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


@login_required(login_url='user:login')
def create_folder(request):
    """
        Handles the creation of a new folder for the logged-in user.

        If the request method is POST, validates the form, creates a folder,
        and associates it with the current user. Optionally, assigns a parent
        folder based on the request.

        Returns:
        - JsonResponse: A response indicating the success or failure of the folder creation.
        """
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.user = request.user

            parent_folder_id = request.POST.get('parent_folder')
            if parent_folder_id:
                folder.parent_folder = get_object_or_404(Folder, id=parent_folder_id, user=request.user)

            folder.save()
            return JsonResponse({
                'success': True,
                'folder': {
                    'id': folder.id,
                    'name': folder.name,
                    'delete_url': reverse_lazy('content:delete_folder', args=[folder.id]),
                }
            })
    return JsonResponse({'success': False})


@login_required(login_url='user:login')
def create_file(request):
    """
        Handles the creation of a new file for the logged-in user.

        If the request method is POST, validates the form, creates a file,
        and associates it with the current user. Optionally, assigns a parent
        folder based on the request.

        Returns:
        - JsonResponse: A response indicating the success or failure of the file creation.
    """
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.user = request.user
            file.size = file.file.size

            parent_folder_id = request.POST.get('parent_folder')
            if parent_folder_id:
                file.folder = get_object_or_404(Folder, id=parent_folder_id, user=request.user)

            file.save()
            return JsonResponse({
                'success': True,
                'file': {
                    'id': file.id,
                    'name': file.name,
                    'thumbnail': file.get_thumbnail_url(),
                    'created_at': file.created_at,
                    'type': file.file_type,
                    'size': file.size,
                    'delete_url': reverse_lazy('content:delete_file', args=[file.id])
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'error': form.errors.as_json()
            })

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


@login_required(login_url='user:login')
def view_folder(request, folder_id):
    """
        Displays the contents of a specific folder, including files and subfolders.

        Fetches the folder based on the provided folder_id and the logged-in user.
        Renders a template displaying files and subfolders within the folder.

        Returns:
        - HttpResponse: The rendered template showing the folder contents.
    """
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)

    files = File.objects.filter(folder=folder)
    sub_folders = Folder.objects.filter(parent_folder=folder)

    return render(request, 'user_files_and_folders.html', { \
        'current_folder': folder,
        'files': files,
        'sub_folders': sub_folders,
    })


@login_required(login_url='user:login')
def user_files_and_folders(request):
    """
       Displays the user's root-level folders and files.

       Fetches all root-level folders (i.e., folders without a parent) and files
       (i.e., files not assigned to a folder) for the logged-in user.
       Renders a template displaying these items.

       Returns:
       - HttpResponse: The rendered template showing the user's files and folders.
       """
    folders = Folder.objects.filter(user=request.user, parent_folder__isnull=True)
    files = File.objects.filter(user=request.user, folder__isnull=True)

    response = render(request, 'user_files_and_folders.html', {
        'folders': folders,
        'files': files,
    })
    response.set_cookie('folder_id', None)
    return response


@login_required(login_url='user:login')
def rename_folder(request, folder_id):
    """
        Renames an existing folder for the logged-in user.

        If the request method is POST, validates the form and renames the folder
        with the provided new name. Returns a JSON response indicating success
        or error.

        Returns:
        - JsonResponse: A response indicating success or error of the rename operation.
        """
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)

    if request.method == 'POST':
        form = RenameFolderForm(request.POST, instance=folder)

        if form.is_valid():
            form.save()

            return JsonResponse({
                "status": "success",
                "message": "Folder renamed successfully!",
                "new_name": form.cleaned_data['name']
            })
        else:
            return JsonResponse({
                "status": "error",
                "error": "Name cannot be empty or invalid."
            })

    return JsonResponse({
        "status": "error",
        "error": "Invalid request."
    })


@login_required(login_url='user:login')
def rename_file(request, file_id):
    """
        Renames an existing file for the logged-in user.

        If the request method is POST, validates the form and renames the file
        with the provided new name. Returns a JSON response indicating success
        or error.

        Returns:
        - JsonResponse: A response indicating success or error of the rename operation.
        """
    file = get_object_or_404(File, id=file_id, user=request.user)

    if request.method == 'POST':
        form = RenameFileForm(request.POST, instance=file)

        if form.is_valid():
            form.save()

            return JsonResponse({
                "status": "success",
                "message": "File renamed successfully!",
                "new_name": form.cleaned_data['name']
            })
        else:
            return JsonResponse({
                "status": "error",
                "error": "Name cannot be empty or invalid."
            })

    return JsonResponse({
        "status": "error",
        "error": "Invalid request."
    })


@login_required(login_url='user:login')
@csrf_exempt
def delete_folder(request, folder_id):
    """
        Deletes a folder and all its contents (files and subfolders) for the logged-in user.

        If the request method is POST, attempts to delete the folder along with its
        files and child folders. Returns a JSON response indicating success or error.

        Returns:
        - JsonResponse: A response indicating success or error of the delete operation.
        """
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)

    if request.method == 'POST':
        try:
            folder_files = File.objects.filter(folder=folder)
            for file in folder_files:
                file.delete()

            child_folders = Folder.objects.filter(parent_folder=folder)
            for child_folder in child_folders:
                delete_folder(request, child_folder.id)

            folder.delete()
            return JsonResponse({"status": "success", "message": "Folder deleted successfully!"})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request method."})


@login_required(login_url='user:login')
@require_POST
def delete_file(request, file_id):
    """
       Deletes a file for the logged-in user.

       If the request method is POST, attempts to delete the file.
       Returns a JSON response indicating success or error.

       Args:
       - request: The HTTP request object.
       - file_id (int): The ID of the file to delete.

       Returns:
       - JsonResponse: A response indicating success or error of the delete operation.
       """
    file = get_object_or_404(File, id=file_id, user=request.user)

    try:
        file.delete()
        return JsonResponse({"status": "success", "message": "File deleted successfully!"})

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@login_required(login_url='user:login')
def search_files(request):
    """
        Searches for files based on the user's query.

        Takes the search query from the GET parameters and filters files
        by name, displaying files that match the query.
.

        Returns:
        - HttpResponse: The rendered template showing search results for files.
        """
    query = request.GET.get('q', '').strip()

    files = []

    if query:
        files = File.objects.filter(
            Q(name__icontains=query) & (Q(folder__isnull=True) | Q(folder__isnull=False)), user=request.user
        )

    return render(request, 'search_results.html', {
        'files': files,
        'query': query
    })


@login_required(login_url='user:login')
def file_detail(request, file_id):
    """
        Provides detailed information about a specific file.

        Fetches the file based on the provided file_id and returns its details
        as a response. If the file doesn't belong to the logged-in user, a 404 error is raised.


        Returns:
        - HttpResponse: The rendered template displaying the file's details.
        """
    file = get_object_or_404(File, id=file_id, user=request.user)
    data = {
        "name": file.name,
        "file_id": file.id,
        "file_type": file.file_type,
        "size": file.size,
        "created_at": file.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": file.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        "thumbnail_url": file.get_thumbnail_url(),
        "file_url": file.file.url,
    }
    return JsonResponse(data)
