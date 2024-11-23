# File and Folder Manager

A Django-based file and folder management system that allows users to register and log in to manage personal folders and files. Users can upload images and videos with volume limits, perform operations like renaming and deleting files or folders, and view file details.  

---

## Features

### User Management
- **Registration**: Create an account using an email address and password.
- **Login/Logout**: Securely authenticate and manage sessions.

### File and Folder Management
- **Folder Management**:
  - Create folders and nested folders.
  - Rename and delete folders.
- **File Management**:
  - Upload image and video files with size restrictions.
  - Open and view files.
  - Display file details (e.g., name, type, size).
  - Rename and delete files.

---

## File Upload Restrictions

- Only **videos** and **images** can be uploaded.
- **File size limits**:
  - Images: Maximum 10 MB.
  - Videos: Maximum 50 MB.
- Supported formats:
  - **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`
  - **Videos**: `.mp4`, `.avi`, `.mov`, `.mkv`

---

## Tech Stack

### Backend
- **Django Framework**
  - `user` app: Handles user registration, login, and logout.
  - `content` app: Manages file and folder operations.

### Frontend
- **HTML, CSS, and JavaScript**: Provides a responsive and user-friendly interface.

### Testing
- **View Tests**: Includes tests for views in the `user` and `content` apps to ensure functionality and reliability.

---
project/
│
├── venv/                 # Virtual environment
├── src/                  # Django project files
│   ├── config/           # Project-level configuration and settings
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py       # Main project URLs
│   │   └── wsgi.py
│   │
│   ├── manage.py         # Django project management script
│   ├── requirements.txt  # Python dependencies
│   │
│   ├── user/             # User app (manages authentication)
│   │   ├── forms.py      # Forms for user app
│   │   ├── urls.py       # URLs for user app
│   │   ├── tests/        # Tests for user app
│   │   ├── views.py
│   │   └── models.py
│   │
│   ├── content/          # Content app (handles files and folders)
│   │   ├── forms.py      # Forms for content app
│   │   ├── urls.py       # URLs for content app
│   │   ├── tests/        # Tests for content app
│   │   ├── views.py
│   │   └── models.py
│   │
│   ├── templates/        # HTML templates for frontend
│   ├── static/           # Static files (CSS, JavaScript, etc.)
│   └── media/            # Uploaded files
│       └── uploads/      # Folder for user-uploaded files
└── README.md             # Project documentation

