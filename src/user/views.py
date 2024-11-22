# views.py
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm


def register_view(request):
    """Handles user registration and login. If the request method is POST, validates the form, creates a new user, sets their password, and logs them in.
       If the registration is successful, the user is redirected to their user files and folders page. If the request method is GET, it simply displays the registration form.

       Process:
       1. If the request method is POST:
          - The form is populated with the submitted data.
          - If the form is valid, the user's password is hashed using set_password(), and the user is saved.
          - A success message is displayed indicating the registration is successful.
          - The user is logged in automatically using the login() method.
          - After logging in, the user is redirected to the "user_files_and_folders" page.
       2. If the request method is GET:
          - The registration form is displayed without any pre-populated data.

       Returns:
       - HttpResponse:
         - A redirect response is returned when the user is successfully registered and logged in.
         - If the form is invalid, the registration page is re-rendered with error messages.
    """

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Registration successful. You can now log in.")
            login(request, user)
            return redirect("content:user_files_and_folders")
    else:
        form = UserRegistrationForm()

    return render(request, "login_register.html", {"form": form})


def login_view(request):
    """Handles user login. It verifies the user's credentials (email and password) through the login form. If the authentication is successful, the user is logged in and redirected to their user files and folders page. If the credentials are incorrect, an error message is displayed.

       Process:
       1. If the request method is POST:
          - The form is populated with the submitted data.
          - If the form is valid, the user is authenticated using the authenticate() function.
          - If authentication is successful, the user is logged in using the login() method and redirected to the "user_files_and_folders" page.
          - If authentication fails, an error message is displayed indicating that the email or password is invalid.
       2. If the request method is GET:
          - The login form is displayed with empty fields.

       Returns:
       - HttpResponse:
         - A redirect response is returned when the user successfully logs in.
         - If the login fails, the login form is re-rendered with error messages.
    """
    error_message = None
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user}!")
                return redirect("content:user_files_and_folders")
            else:
                # messages.error(request, "Invalid email or password.")
                error_message = "Invalid email or password."
    else:
        form = UserLoginForm()

    return render(request, "login_register.html", {"form": form, "error_message": error_message})


def logout_view(request):
    """Logs out the current user, invalidates their session, and redirects them to the login page. A success message is displayed indicating that the user has been logged out.
       Returns:
       - HttpResponse:
         - A redirect response is returned to the login page after logging out.
    """
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("user:login")
