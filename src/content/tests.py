from django.test import TestCase
from django.urls import reverse, reverse_lazy
from user.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from content.models import Folder, File
from django.utils import timezone



class FileAndFolderTests(TestCase):

    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(
            email='test@test.com', password='password123')
        self.client.login(email='test@test.com', password='password123')

        # Create a folder for the user
        self.folder = Folder.objects.create(
            name='Test Folder', user=self.user, parent_folder=None)

        # Prepare a test file to upload
        self.test_file = SimpleUploadedFile(
            'testfile.png', b'file_content', content_type='image/png')

    def test_create_folder(self):
        url = reverse('content:create_folder')
        data = {'name': 'New Folder', 'parent_folder': self.folder.id}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])

        # Check if the folder is created in the database
        new_folder = Folder.objects.get(name='New Folder')
        self.assertEqual(new_folder.user, self.user)

    def test_create_file(self):
        url = reverse_lazy('content:create_file')
        data = {'name': 'Test File', 'file': self.test_file, 'parent_folder': self.folder.id}

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])

        # Check if the file is saved in the database
        file = File.objects.get(name='Test File')
        self.assertEqual(file.user, self.user)

    def test_rename_folder(self):
        url = reverse('content:rename_folder', args=[self.folder.id])
        data = {'name': 'Renamed Folder'}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(response.json()['new_name'], 'Renamed Folder')

        # Verify if folder name is updated in the database
        renamed_folder = Folder.objects.get(id=self.folder.id)
        self.assertEqual(renamed_folder.name, 'Renamed Folder')

    def test_rename_file(self):
        file = File.objects.create(
            name='Test File', user=self.user, folder=self.folder, file=self.test_file, size=len(self.test_file.read()))

        url = reverse('content:rename_file', args=[file.id])
        data = {'name': 'Renamed Test File'}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(response.json()['new_name'], 'Renamed Test File')

        # Verify if file name is updated in the database
        renamed_file = File.objects.get(id=file.id)
        self.assertEqual(renamed_file.name, 'Renamed Test File')

    def test_delete_folder(self):
        url = reverse('content:delete_folder', args=[self.folder.id])

        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')

        # Verify if the folder is deleted from the database
        with self.assertRaises(Folder.DoesNotExist):
            Folder.objects.get(id=self.folder.id)

    def test_delete_file(self):
        file = File.objects.create(
            name='Test File', user=self.user, folder=self.folder, file=self.test_file, size=len(self.test_file.read()))

        url = reverse('content:delete_file', args=[file.id])

        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')

        # Verify if the file is deleted from the database
        with self.assertRaises(File.DoesNotExist):
            File.objects.get(id=file.id)

    def test_view_folder(self):
        url = reverse('content:view_folder', args=[self.folder.id])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_files_and_folders.html')
        self.assertIn('current_folder', response.context)
        self.assertIn('files', response.context)
        self.assertIn('sub_folders', response.context)

    def test_user_files_and_folders(self):
        url = reverse('content:user_files_and_folders')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('folders', response.context)
        self.assertIn('files', response.context)

    def test_search_files(self):
        file = File.objects.create(
            name='Test File', user=self.user, folder=self.folder, file=self.test_file, size=len(self.test_file.read()))

        url = reverse('content:search_files')
        response = self.client.get(url, {'q': 'Test File'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('files', response.context)
        self.assertEqual(len(response.context['files']), 1)
        self.assertEqual(response.context['files'][0], file)

    def test_file_detail(self):
        file = File.objects.create(
            name='Test File', user=self.user, folder=self.folder, file=self.test_file, size=len(self.test_file.read()))

        url = reverse('content:file_detail', args=[file.id])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            "name": file.name,
            "file_id": file.id,
            "file_type": file.file_type,
            "size": file.size,
            "created_at": file.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": file.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            "thumbnail_url": file.get_thumbnail_url(),
            "file_url": file.file.url,
        })
