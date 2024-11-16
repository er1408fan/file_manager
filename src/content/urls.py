from django.conf.urls.static import static
from django.urls import path

from config import settings
from . import views

app_name = 'content'

urlpatterns = [
    path('files/create/', views.create_file, name='create_file'),
    path('folders/create/', views.create_folder, name='create_folder'),
    path('folders/<int:folder_id>/', views.view_folder, name='view_folder'),
    path('', views.user_files_and_folders, name='user_files_and_folders'),
    path('folders/<int:folder_id>/rename/', views.rename_folder, name='rename_folder'),
    path('files/<int:file_id>/rename/', views.rename_file, name='rename_file'),
    path('folders/<int:folder_id>/delete/', views.delete_folder, name='delete_folder'),
    path('files_delete/<int:file_id>/delete/', views.delete_file, name='delete_file'),
    path('files_detail/<int:file_id>', views.file_detail, name='file_detail'),
    path('search/', views.search_files, name='search_files'),
]



