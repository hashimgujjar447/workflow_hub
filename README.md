# WorkflowHub 🚀

A robust team workflow management system built with Django 6.0. WorkflowHub helps teams organize work using a hierarchy: **Workspaces → Projects → Tasks**, featuring secure authentication, role-based access, threaded comments, and a full-featured REST API.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Django](https://img.shields.io/badge/Django-6.0-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightblue)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📑 Table of Contents

1. [Overview](#overview)
2. [Features](#-features)
3. [Tech Stack](#-tech-stack)
4. [Project Structure](#-project-structure)
5. [Application Architecture](#-application-architecture)
6. [Database Models](#-database-models-detailed)
7. [URL Routes](#-url-routes)
8. [Views & Business Logic](#-views--business-logic)
9. [Templates](#-templates)
10. [Authentication System](#-authentication-system)
11. [REST API](#-rest-api)
12. [Installation Guide](#-installation-guide)
13. [Configuration](#-configuration)
14. [Usage Guide](#-usage-guide)
15. [Contributing](#-contributing)

---

## Overview

WorkflowHub is a Django-based platform for team project management. It uses a hierarchical data model:

```
User → Workspace → Project → Task → Comment
```

**Concepts:**
- **Workspace:** Top-level container for teams and projects
- **Project:** Initiative within a workspace
- **Task:** Work item assigned to project members
- **Comment:** Threaded discussion on tasks

---

## 📋 Features

- **User Authentication:** Custom user model, email-based login, registration, secure routes
- **Workspace Management:** Unlimited workspaces, unique slugs, member roles, project tracking
- **Project Management:** Projects within workspaces, status tracking, role-based membership
- **Task Management:** Tasks within projects, assignment, status workflow, due dates
- **Comments & Collaboration:** Threaded comments, nested replies, author tracking
- **REST API:** Full-featured RESTful API with JWT authentication, workspace/project/task/comment endpoints
- **Modern UI:** Responsive design, CSS variables, sidebar navigation, status badges

---

## 🛠️ Tech Stack

| Category            | Technology                  |
|---------------------|----------------------------|
| Backend Framework   | Django 6.0.1               |
| API Framework       | Django REST Framework      |
| Authentication      | JWT (Simple JWT)           |
| Database            | SQLite                     |
| Frontend            | HTML5, CSS3, JavaScript    |
| CSS Architecture    | Custom CSS with Variables  |
| Python Version      | Python 3.x                 |
| Debug Tools         | Django Debug Toolbar 6.2.0 |

**Dependencies:**
```
Django==6.0.1
asgiref==3.11.0
sqlparse==0.5.5
tzdata==2025.3
django-debug-toolbar==6.2.0
djangorestframework
djangorestframework-simplejwt
```

---

## 📁 Project Structure

```
workflow_management_system/
│
├── manage.py
├── db.sqlite3
├── README.md
│
├── workflow_hub/
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── workspaces/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── projects/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── tasks/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── comments/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── api/
│   ├── urls.py
│   ├── serializers/
│   │   ├── workspace.py
│   │   ├── workspace_members.py
│   │   ├── workspace_projects.py
│   │   ├── task_serializers.py
│   │   ├── comment_serializer.py
│   │   ├── comment_reply_serializer.py
│   │   └── common_serializers.py
│   └── views/
│       ├── workspace.py
│       ├── workspace_members.py
│       ├── workspace_projects.py
│       ├── project_task_details.py
│       └── task_comments.py
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── accounts/
│   ├── workspaces/
│   ├── projects/
│   ├── tasks/
│   ├── task/
│   └── includes/
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── index.js
│
└── env/
```

---

## 🏛️ Application Architecture

### Django Apps Overview

```
workflow_hub (settings, urls, views)
│
├── accounts (auth)
├── workspaces (team spaces)
├── projects (project mgmt)
├── tasks (work items)
├── comments (discussions)
└── api (REST API)
```

### Request Flow

```
User Request
    │
    ▼
URL Router → Middleware → Views (@login_required) → Models → Templates → HTTP Response
```

---

## 🗃️ Database Models (Detailed)

### Entity Relationship Diagram

```
Account ──▶ Workspace ──▶ Project ──▶ Task ──▶ TaskComment
     │           │             │           │         ▲
     │           │             │           │         │
WorkspaceMember ProjectMember             │         │
                                  (self-referencing for replies)
```

---

### 1. Account Model

Custom user model with email authentication.

```python
class Account(AbstractBaseUser):
        first_name = CharField(max_length=50)
        last_name = CharField(max_length=50)
        username = CharField(max_length=100, unique=True)
        email = EmailField(max_length=100, unique=True)
        phone_number = CharField(max_length=50, blank=True)
        date_joined = DateTimeField(auto_now_add=True)
        last_login = DateTimeField(auto_now=True)
        is_admin = BooleanField(default=False)
        is_staff = BooleanField(default=False)
        is_active = BooleanField(default=True)
        is_superadmin = BooleanField(default=False)
        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
```

---

### 2. Workspace Model

```python
class Workspace(Model):
        name = CharField(max_length=100)
        slug = SlugField(max_length=100, unique=True)
        creator = ForeignKey(Account, on_delete=CASCADE, related_name='created_workspaces')
        is_active = BooleanField(default=True)
        created_at = DateTimeField(auto_now_add=True)
        updated_at = DateTimeField(auto_now=True)
```

---

### 3. WorkspaceMember Model

```python
class WorkspaceMember(Model):
        ROLE_CHOICES = (
                ('manager', 'Manager'),
                ('leader', 'Leader'),
                ('frontend', 'Frontend Developer'),
                ('backend', 'Backend Developer'),
                ('seo', 'SEO'),
        )
        workspace = ForeignKey(Workspace, on_delete=CASCADE, related_name='members')
        user = ForeignKey(Account, on_delete=CASCADE, related_name='workspace_memberships')
        role = CharField(max_length=20, choices=ROLE_CHOICES)
        joined_at = DateTimeField(auto_now_add=True)
        is_active = BooleanField(default=True)
        class Meta:
                unique_together = ('workspace', 'user')
```

---

### 4. Project Model

```python
class Project(Model):
        STATUS_CHOICES = (
                ('pending', 'Pending'),
                ('in_progress', 'In Progress'),
                ('completed', 'Completed'),
                ('failed', 'Failed'),
        )
        workspace = ForeignKey(Workspace, on_delete=CASCADE, related_name='projects')
        name = CharField(max_length=150)
        slug = SlugField(max_length=150)
        status = CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
        created_by = ForeignKey(Account, on_delete=SET_NULL, null=True, related_name='created_projects')
        is_active = BooleanField(default=True)
        created_at = DateTimeField(auto_now_add=True)
        updated_at = DateTimeField(auto_now=True)
        class Meta:
                unique_together = ('workspace', 'slug')
                ordering = ['-created_at']
```

---

### 5. ProjectMember Model

```python
class ProjectMember(Model):
        ROLE_CHOICES = (
                ('manager', 'Manager'),
                ('leader', 'Leader'),
                ('frontend', 'Frontend Developer'),
                ('backend', 'Backend Developer'),
                ('seo', 'SEO'),
        )
        member = ForeignKey(Account, on_delete=CASCADE, related_name='project_memberships')
        project = ForeignKey(Project, on_delete=CASCADE, related_name='members')
        role = CharField(max_length=50, choices=ROLE_CHOICES)
        is_active = BooleanField(default=True)
        joined_at = DateTimeField(auto_now_add=True)
        updated_at = DateTimeField(auto_now=True)
        class Meta:
                unique_together = ('project', 'member')
```

---

### 6. Task Model

```python
class Task(Model):
        STATUS_CHOICES = (
                ('todo', 'To Do'),
                ('in_progress', 'In Progress'),
                ('review', 'Review'),
                ('completed', 'Completed'),
                ('failed', 'Failed'),
        )
        project = ForeignKey(Project, on_delete=CASCADE, related_name='tasks')
        title = CharField(max_length=200)
        description = TextField(blank=True)
        assigned_to = ForeignKey(ProjectMember, on_delete=SET_NULL, null=True, blank=True, related_name='tasks')
        created_by = ForeignKey(Account, on_delete=SET_NULL, null=True, related_name='created_tasks')
        status = CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
        due_date = DateField(null=True, blank=True)
        created_at = DateTimeField(auto_now_add=True)
        updated_at = DateTimeField(auto_now=True)
```

---

### 7. TaskComment Model

```python
class TaskComment(Model):
        task = ForeignKey(Task, on_delete=CASCADE, related_name='comments')
        author = ForeignKey(Account, on_delete=SET_NULL, null=True, related_name='task_comments')
        parent_comment = ForeignKey('self', on_delete=CASCADE, null=True, blank=True, related_name='replies')
        content = TextField()
        created_at = DateTimeField(auto_now_add=True)
        updated_at = DateTimeField(auto_now=True)
```

---

## 🔗 URL Routes

### Web Application Routes

- **Root URLs:** `/`, `/admin/`, `/accounts/*`, `/workspace/*`, `/projects/*`, `/tasks/*`, `/__debug__/*`
- **Accounts:** `/accounts/login/`, `/accounts/register/`, `/accounts/logout/`, `/accounts/profile/`
- **Workspaces:** `/workspace/`, `/workspace/create/`, `/workspace/<slug>/`, `/workspace/<slug>/add_member/`, `/workspace/<slug>/create_project/`, `/workspace/<slug>/settings/`
- **Projects:** `/projects/`, `/projects/<ws_slug>/<proj_slug>/`, `/projects/<ws_slug>/<proj_slug>/add_new_member`, `/projects/<ws_slug>/<proj_slug>/task/*`, `/projects/<ws_slug>/<proj_slug>/comment/*`
- **Tasks:** `/tasks/get_all_tasks/`, `/.../task/add_task`
- **Comments:** `/.../comment/<id>/`

### REST API Routes

- **Authentication:**
  - `POST /api/token/` - Obtain JWT token pair
  - `POST /api/token/refresh/` - Refresh access token

- **Workspaces:**
  - `GET /api/workspaces/` - List user's workspaces
  - `POST /api/workspaces/` - Create new workspace
  - `GET /api/workspaces/<slug>/` - Retrieve workspace details
  - `PUT/PATCH /api/workspaces/<slug>/` - Update workspace
  - `DELETE /api/workspaces/<slug>/` - Delete workspace

- **Workspace Members:**
  - `GET /api/workspaces/<slug>/members/` - List workspace members
  - `POST /api/workspaces/<slug>/members/` - Add member to workspace

- **Projects:**
  - `GET /api/workspaces/<slug>/projects/` - List workspace projects
  - `POST /api/workspaces/<slug>/projects/` - Create project in workspace
  - `GET /api/workspaces/<slug>/projects/<project_slug>/` - Retrieve project details
  - `PUT/PATCH /api/workspaces/<slug>/projects/<project_slug>/` - Update project
  - `DELETE /api/workspaces/<slug>/projects/<project_slug>/` - Delete project

- **Tasks:**
  - `GET /api/workspaces/<slug>/projects/<project_slug>/tasks/` - List project tasks
  - `GET /api/workspaces/<slug>/projects/<project_slug>/tasks/<id>/` - Retrieve task details

- **Comments:**
  - `GET /api/workspaces/<slug>/projects/<project_slug>/tasks/<id>/comments/` - List task comments
  - `POST /api/workspaces/<slug>/projects/<project_slug>/tasks/<id>/comments/` - Add comment to task

---

## 🎯 Views & Business Logic

- **Authentication:** Login, register, logout views; email/password authentication
- **Workspace:** List, create, detail, add member, create project, settings
- **Project:** List, detail, add member
- **Task:** Dashboard, create task, list tasks
- **Comment:** View/add comments, threaded replies
- **API Views:** RESTful views for all resources with permissions

---

## 📄 Templates

- **base.html:** Master layout, sidebar, navigation
- **home.html:** Dashboard
- **accounts:** Login/register/profile templates
- **workspaces:** List, create, detail, add member, create project, settings
- **projects:** List, detail, create, add member
- **tasks:** Create task, all tasks
- **task:** Task dashboard, comments, reusable fragments

---

## 🔐 Authentication System

### Web Authentication
- Custom user model (`AUTH_USER_MODEL = 'accounts.Account'`)
- Email-based login (USERNAME_FIELD = 'email')
- All views protected with `@login_required`
- Login/logout redirects configured in `settings.py`

### API Authentication
- **JWT (JSON Web Tokens)** via djangorestframework-simplejwt
- **Session Authentication** for browsable API
- All API endpoints require authentication (`IsAuthenticated` permission)
- Token obtain: `POST /api/token/` with email and password
- Token refresh: `POST /api/token/refresh/` with refresh token

---

## 🌐 REST API

### Overview

WorkflowHub provides a comprehensive RESTful API built with Django REST Framework, featuring JWT authentication and full CRUD operations for all resources.

### API Features

- **Authentication:** JWT token-based authentication
- **Permissions:** All endpoints require authentication
- **Serialization:** JSON request/response format
- **Browsable API:** Interactive API documentation at `/api/`
- **Pagination:** Configurable pagination for list endpoints
- **Nested Resources:** Hierarchical resource structure (workspace → project → task → comment)

### API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/token/` | Obtain JWT token |
| POST | `/api/token/refresh/` | Refresh access token |
| GET/POST | `/api/workspaces/` | List/Create workspaces |
| GET/PUT/DELETE | `/api/workspaces/<slug>/` | Workspace details |
| GET/POST | `/api/workspaces/<slug>/members/` | Workspace members |
| GET/POST | `/api/workspaces/<slug>/projects/` | List/Create projects |
| GET/PUT/DELETE | `/api/workspaces/<slug>/projects/<slug>/` | Project details |
| GET | `/api/workspaces/<slug>/projects/<slug>/tasks/` | List tasks |
| GET | `/api/workspaces/<slug>/projects/<slug>/tasks/<id>/` | Task details |
| GET/POST | `/api/workspaces/<slug>/projects/<slug>/tasks/<id>/comments/` | Task comments |

### API Response Format

Successful responses include relevant data with appropriate HTTP status codes:
- `200 OK` - Successful GET/PUT/PATCH
- `201 Created` - Successful POST
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Validation errors
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource not found

---

## 🚀 Installation Guide

1. **Clone:** `git clone https://github.com/yourusername/workflow_management_system.git`
2. **Navigate:** `cd workflow_management_system`
3. **Virtual Env:** `python -m venv env` & activate
   - Windows: `env\Scripts\activate`
   - Unix/Mac: `source env/bin/activate`
4. **Install Dependencies:** 
   ```bash
   pip install django==6.0.1
   pip install django-debug-toolbar
   pip install djangorestframework
   pip install djangorestframework-simplejwt
   ```
5. **Migrate Database:** `python manage.py migrate`
6. **Create Superuser:** `python manage.py createsuperuser`
7. **Run Server:** `python manage.py runserver`
8. **Access Application:** 
   - Web UI: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/
   - API: http://127.0.0.1:8000/api/

---

## ⚙️ Configuration

### Core Settings
- `SECRET_KEY`: Django secret key (change in production)
- `DEBUG`: Set to `True` for development, `False` for production
- `ALLOWED_HOSTS`: List of allowed hostnames
- `DATABASES`: SQLite database configuration
- `STATIC_URL`: Static files URL configuration
- `AUTH_USER_MODEL`: `'accounts.Account'` (custom user model)
- `LOGIN_URL`: `'login'`
- `LOGIN_REDIRECT_URL`: `'home'`
- `LOGOUT_REDIRECT_URL`: `'login'`

### Installed Apps
- Django core apps (admin, auth, contenttypes, sessions, messages, staticfiles)
- Custom apps: accounts, workspaces, projects, tasks, comments, api
- Third-party: debug_toolbar, rest_framework

### REST Framework Configuration
```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}
```

---

## 📖 Usage Guide

### Web Application

1. **Register:** Navigate to `/accounts/register/` and create an account
2. **Login:** Use your email and password at `/accounts/login/`
3. **Create Workspace:** Go to `/workspace/create/` to set up your team workspace
4. **Add Members:** Invite team members with roles (Manager, Leader, Frontend, Backend, SEO)
5. **Create Project:** Within a workspace, create projects with status tracking
6. **Add Tasks:** Create tasks within projects, assign to team members, set due dates
7. **Collaborate:** Add comments to tasks, reply to comments for threaded discussions
8. **Manage:** Use workspace settings to manage team and projects

### REST API Usage

1. **Obtain Token:**
   ```bash
   curl -X POST http://127.0.0.1:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "yourpassword"}'
   ```

2. **Make Authenticated Requests:**
   ```bash
   curl -X GET http://127.0.0.1:8000/api/workspaces/ \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
   ```

3. **Create Workspace:**
   ```bash
   curl -X POST http://127.0.0.1:8000/api/workspaces/ \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"name": "My Workspace"}'
   ```

4. **Browse API:** Visit http://127.0.0.1:8000/api/ in your browser for the browsable API interface

---

## 🎨 CSS Theme Variables

```css
:root {
        --primary: #4F46E5;
        --primary-hover: #4338CA;
        --text-heading: #1F2937;
        --text-body: #4B5563;
        --text-muted: #9CA3AF;
        --bg-main: #F9FAFB;
        --bg-card: #FFFFFF;
        --bg-sidebar: #1F2937;
        --border-color: #E5E7EB;
        --success: #16A34A;
        --in-progress: #3B82F6;
        --review: #F59E0B;
        --danger: #DC2626;
}
```

---

## 🔜 Roadmap / Future Features

- ✅ ~~REST API~~ (Implemented)
- Email notifications
- File attachments
- Audit logs
- Analytics & charts
- Kanban board
- Real-time updates (WebSockets)
- Export tasks (PDF, CSV)
- Calendar view
- Advanced search & filtering
- Task dependencies
- Time tracking
- Mobile app

---

## 🤝 Contributing

1. Fork the repo
2. Create a branch
3. Commit changes
4. Push branch
5. Open Pull Request

**Code Style:** PEP 8, meaningful names, docstrings, thin views

---

## 📄 License

MIT License - see [LICENSE](LICENSE).

---

## 👨‍💻 Author

Built with ❤️ using Django

---

⭐ **If you found this project helpful, please give it a star!**
