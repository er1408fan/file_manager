from django.test import TestCase
from django.urls import reverse, reverse_lazy
from .forms import UserRegistrationForm
from .models import User
from django.contrib.messages import get_messages


class UserLogoutViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='securepassword123')
        self.client.login(email='testuser@example.com', password='securepassword123')
        self.url = reverse_lazy('user:logout')  # Replace with your actual URL name for the logout view

    def test_logout_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Should redirect after logout
        self.assertRedirects(response, reverse_lazy('user:login'))  # Adjust to your login URL

        # Check logout success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'You have been logged out.')


class UserLoginViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='securepassword123')
        self.url = reverse('user:login')  # Replace with your actual URL name for the login view

    def test_login_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login_register.html')
        self.assertContains(response, 'Login')

    def test_login_view_post_valid(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'securepassword123',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Should redirect after successful login
        self.assertRedirects(response, reverse('content:user_files_and_folders'))  # Adjust to your post-login URL

        # Check login success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Welcome back, testuser@example.com!')


class UserRegistrationViewTest(TestCase):

    def setUp(self):
        self.url = reverse_lazy('user:register')  # Replace with your actual URL name for the register view

    def test_register_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login_register.html')
        self.assertContains(response, 'Register')

    def test_register_view_post_valid(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'securepassword123',
            'confirm_password': 'securepassword123',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Should redirect after successful registration
        self.assertRedirects(response, reverse_lazy('content:user_files_and_folders'))  # Adjust to your post-login URL

        # Verify the user is created
        user = User.objects.get(email='testuser@example.com')
        self.assertTrue(user.check_password('securepassword123'))

        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Registration successful. You can now log in.")

    # Testing the UserRegistrationForm validation directly
    def test_passwords_match_in_registration_form(self):
        form_data = {
            'email': 'testuser@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_passwords_do_not_match_in_registration_form(self):
        form_data = {
            'email': 'testuser@example.com',
            'password': 'password123',
            'confirm_password': 'differentpassword123',
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Passwords do not match.', form.errors['__all__'])
