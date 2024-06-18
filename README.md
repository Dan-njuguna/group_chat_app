# Group Chat Application in Django

- To use the Chat API, follow the following steps:
  1) Create a virtual environment.
  2) Navigate to templates and static folder at the root of the directory.
  3) Link your templates and static files.


## Directory Structure

```markdown
core/
│
├── core/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── templates/
│   ├── chat/
│   │   └── chat.html
│   ├── usersignin/
│   │   └── signup.html
│
├── usersignin/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
│
├── chat/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
│
├── manage.py
└── requirements.txt
```

### Description

- **core/**: Contains the main Django project folder.
- **core/core/**: Inner core directory containing project settings (`settings.py`), URLs (`urls.py`), WSGI and ASGI configuration (`wsgi.py`, `asgi.py`).
- **templates/**: Directory for HTML templates, organized by application (`chat/`, `usersignin/`).
- **usersignin/**: Django app for user sign-up functionality, including admin, forms, models, tests, and views.
- **chat/**: Django app for chat functionality, including admin, models, tests, and views.
- **manage.py**: Django's command-line utility for managing the project.
- **requirements.txt**: File listing Python dependencies for the project.
