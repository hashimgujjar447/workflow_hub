# WorkflowHub 🚀

A comprehensive team workflow management system built with Django 6.0. WorkflowHub enables teams to organize their work through a hierarchical structure of **Workspaces → Projects → Tasks**, with robust user authentication, role-based access control, and threaded commenting.

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
11. [Installation Guide](#-installation-guide)
12. [Configuration](#-configuration)
13. [Usage Guide](#-usage-guide)
14. [Contributing](#-contributing)

---

## Overview

WorkflowHub is a Django-based project management platform designed for teams. It follows a hierarchical data model:

```
User → Workspace → Project → Task → Comment
```

**Key Concepts:**
- **Workspace**: Top-level container for organizing teams and projects (like an organization)
- **Project**: A specific initiative within a workspace with its own team members
- **Task**: Individual work items assigned to project members
- **Comment**: Discussion threads on tasks with nested reply support

---

## 📋 Features

### 🔐 User Authentication
- Custom user model with email-based authentication
- User registration with validation (email uniqueness, password confirmation)
- Secure login/logout functionality
- Protected routes requiring authentication

### 🏢 Workspace Management
- Create unlimited workspaces
- Auto-generated unique slugs for URLs
- Add team members with specific roles
- View all projects within a workspace
- Track member count and project count

### 📁 Project Management
- Create projects within workspaces
- Project status tracking (Pending, In Progress, Completed, Failed)
- Assign project members from workspace members
- Role-based project membership
- Unique project slugs scoped to workspace

### ✅ Task Management
- Create tasks within projects
- Assign tasks to project members
- Task status workflow (To Do → In Progress → Review → Completed/Failed)
- Due date tracking
- View tasks assigned to you vs. tasks created by you
- Rich task descriptions

### 💬 Comments & Collaboration
- Add comments on any task
- Threaded replies (nested comments)
- Track comment author and timestamps
- PRG (Post-Redirect-Get) pattern to prevent duplicate submissions

### 🎨 Modern UI
- Clean, responsive design
- CSS Variables for theming
- Sidebar navigation
- Status badges with color coding
- Mobile-friendly layout

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| **Backend Framework** | Django 6.0.1 |
| **Database** | SQLite (development) |
| **Frontend** | HTML5, CSS3, JavaScript |
| **CSS Architecture** | Custom CSS with CSS Variables |
| **Python Version** | Python 3.x |
| **Debug Tools** | Django Debug Toolbar 6.2.0 |

### Dependencies
```
Django==6.0.1
asgiref==3.11.0
sqlparse==0.5.5
tzdata==2025.3
django-debug-toolbar==6.2.0
```

---

## 📁 Project Structure

```
workflow_management_system/
│
├── manage.py                 # Django management script
├── db.sqlite3               # SQLite database file
├── README.md                # This documentation
│
├── workflow_hub/            # Main Django project configuration
│   ├── __init__.py
│   ├── settings.py          # Project settings (apps, middleware, database, etc.)
│   ├── urls.py              # Root URL configuration
│   ├── views.py             # Home page view
│   ├── wsgi.py              # WSGI application entry point
│   └── asgi.py              # ASGI application entry point
│
├── accounts/                # User authentication app
│   ├── models.py            # Custom Account model
│   ├── views.py             # Login, register, logout views
│   ├── urls.py              # Auth-related URLs
│   └── admin.py             # Admin site registration
│
├── workspaces/              # Workspace management app
│   ├── models.py            # Workspace, WorkspaceMember models
│   ├── views.py             # Workspace CRUD operations
│   ├── urls.py              # Workspace URLs
│   └── admin.py             # Admin registration
│
├── projects/                # Project management app
│   ├── models.py            # Project, ProjectMember models
│   ├── views.py             # Project operations
│   ├── urls.py              # Project URLs (includes tasks & comments)
│   └── admin.py             # Admin registration
│
├── tasks/                   # Task management app
│   ├── models.py            # Task model
│   ├── views.py             # Task creation, listing
│   ├── urls.py              # Task URLs
│   └── admin.py             # Admin registration
│
├── comments/                # Comments & replies app
│   ├── models.py            # TaskComment model (self-referencing)
│   ├── views.py             # Comment operations
│   ├── urls.py              # Comment URLs
│   └── admin.py             # Admin registration
│
├── templates/               # HTML templates
│   ├── base.html            # Base layout with sidebar
│   ├── home.html            # Dashboard/home page
│   ├── accounts/            # Auth templates (login, register)
│   ├── workspaces/          # Workspace templates
│   ├── projects/            # Project templates
│   ├── tasks/               # Task creation templates
│   ├── task/                # Task listing & comments templates
│   └── includes/            # Reusable template fragments
│
├── static/                  # Static assets
│   ├── css/
│   │   └── style.css        # Main stylesheet (2200+ lines)
│   └── js/
│       └── index.js         # JavaScript functionality
│
└── env/                     # Virtual environment (not committed)
```

---

## 🏛️ Application Architecture

### Django Apps Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        workflow_hub                              │
│                    (Project Configuration)                       │
│         settings.py │ urls.py │ views.py │ wsgi.py              │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   accounts    │    │  workspaces   │    │   projects    │
│ (Custom Auth) │    │ (Team Spaces) │    │(Project Mgmt) │
└───────────────┘    └───────────────┘    └───────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                                           │
        ▼                                           ▼
┌───────────────┐                          ┌───────────────┐
│    tasks      │◄─────────────────────────│   comments    │
│ (Work Items)  │                          │(Discussions)  │
└───────────────┘                          └───────────────┘
```

### Request Flow

```
User Request
     │
     ▼
┌─────────────────┐
│   URL Router    │  (workflow_hub/urls.py)
│   /workspace/*  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Middleware    │  (Auth, CSRF, Session, Debug Toolbar)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     Views       │  (Business Logic)
│ @login_required │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     Models      │  (Database Operations)
│   ORM Queries   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Templates     │  (HTML Rendering)
│   + Context     │
└────────┬────────┘
         │
         ▼
   HTTP Response
```

---

## 🗃️ Database Models (Detailed)

### Entity Relationship Diagram

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│    ┌─────────────┐         ┌─────────────────┐         ┌─────────────────┐  │
│    │   Account   │────────▶│    Workspace    │────────▶│     Project     │  │
│    │  (User)     │ creates │                 │ contains│                 │  │
│    └─────────────┘         └─────────────────┘         └─────────────────┘  │
│          │                        │                           │             │
│          │                        │                           │             │
│          │ member_of              │ has_members               │ has_members │
│          │                        │                           │             │
│          ▼                        ▼                           ▼             │
│    ┌─────────────┐         ┌─────────────────┐         ┌─────────────────┐  │
│    │  (through)  │         │WorkspaceMember  │         │ ProjectMember   │  │
│    │             │         │  user + role    │         │  member + role  │  │
│    └─────────────┘         └─────────────────┘         └─────────────────┘  │
│                                                               │             │
│                                                               │ has_tasks   │
│                                                               ▼             │
│                                                        ┌─────────────────┐  │
│                                                        │      Task       │  │
│                                                        │ assigned_to     │  │
│                                                        │ created_by      │  │
│                                                        └─────────────────┘  │
│                                                               │             │
│                                                               │ has_comments│
│                                                               ▼             │
│                                                        ┌─────────────────┐  │
│                                                        │  TaskComment    │──┐│
│                                                        │   (author)      │  ││
│                                                        └─────────────────┘  ││
│                                                               ▲             ││
│                                                               │ replies     ││
│                                                               └─────────────┘│
└──────────────────────────────────────────────────────────────────────────────┘
```

---

### 1. Account Model (`accounts/models.py`)

Custom user model extending Django's `AbstractBaseUser` with email-based authentication.

```python
class Account(AbstractBaseUser):
    # Fields
    first_name      = CharField(max_length=50)
    last_name       = CharField(max_length=50)
    username        = CharField(max_length=100, unique=True)
    email           = EmailField(max_length=100, unique=True)  # Primary identifier
    phone_number    = CharField(max_length=50, blank=True)
    
    # Timestamps
    date_joined     = DateTimeField(auto_now_add=True)
    last_login      = DateTimeField(auto_now=True)
    
    # Permissions
    is_admin        = BooleanField(default=False)
    is_staff        = BooleanField(default=False)
    is_active       = BooleanField(default=True)
    is_superadmin   = BooleanField(default=False)
    
    USERNAME_FIELD  = 'email'  # Login with email, not username
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
```

**Key Features:**
- Email is the primary authentication field (`USERNAME_FIELD = 'email'`)
- Custom `AccountManager` for user creation
- Support for superuser creation via `createsuperuser` command
- Natural key support via `get_by_natural_key()`

---

### 2. Workspace Model (`workspaces/models.py`)

Top-level organizational container.

```python
class Workspace(Model):
    name        = CharField(max_length=100)
    slug        = SlugField(max_length=100, unique=True)  # URL-friendly identifier
    creator     = ForeignKey(Account, on_delete=CASCADE, related_name='created_workspaces')
    is_active   = BooleanField(default=True)
    created_at  = DateTimeField(auto_now_add=True)
    updated_at  = DateTimeField(auto_now=True)
```

**Relationships:**
- `creator` → One-to-Many with Account (one user can create many workspaces)
- `members` → Via `WorkspaceMember` through model
- `projects` → One-to-Many reverse relation

---

### 3. WorkspaceMember Model (`workspaces/models.py`)

Links users to workspaces with role assignment.

```python
class WorkspaceMember(Model):
    ROLE_CHOICES = (
        ('manager', 'Manager'),
        ('leader', 'Leader'),
        ('frontend', 'Frontend Developer'),
        ('backend', 'Backend Developer'),
        ('seo', 'SEO'),
    )
    
    workspace   = ForeignKey(Workspace, on_delete=CASCADE, related_name='members')
    user        = ForeignKey(Account, on_delete=CASCADE, related_name='workspace_memberships')
    role        = CharField(max_length=20, choices=ROLE_CHOICES)
    joined_at   = DateTimeField(auto_now_add=True)
    is_active   = BooleanField(default=True)
    
    class Meta:
        unique_together = ('workspace', 'user')  # User can only be member once per workspace
```

---

### 4. Project Model (`projects/models.py`)

Projects live within workspaces.

```python
class Project(Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    
    workspace   = ForeignKey(Workspace, on_delete=CASCADE, related_name='projects')
    name        = CharField(max_length=150)
    slug        = SlugField(max_length=150)  # Unique within workspace
    status      = CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_by  = ForeignKey(Account, on_delete=SET_NULL, null=True, related_name='created_projects')
    is_active   = BooleanField(default=True)
    created_at  = DateTimeField(auto_now_add=True)
    updated_at  = DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('workspace', 'slug')  # Slug unique per workspace
        ordering = ['-created_at']
```

---

### 5. ProjectMember Model (`projects/models.py`)

Links users to projects with role assignment.

```python
class ProjectMember(Model):
    ROLE_CHOICES = (...)  # Same as WorkspaceMember
    
    member      = ForeignKey(Account, on_delete=CASCADE, related_name='project_memberships')
    project     = ForeignKey(Project, on_delete=CASCADE, related_name='members')
    role        = CharField(max_length=50, choices=ROLE_CHOICES)
    is_active   = BooleanField(default=True)
    joined_at   = DateTimeField(auto_now_add=True)
    updated_at  = DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('project', 'member')
```

---

### 6. Task Model (`tasks/models.py`)

Individual work items within projects.

```python
class Task(Model):
    STATUS_CHOICES = (
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('review', 'Review'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    
    project     = ForeignKey(Project, on_delete=CASCADE, related_name='tasks')
    title       = CharField(max_length=200)
    description = TextField(blank=True)
    assigned_to = ForeignKey(ProjectMember, on_delete=SET_NULL, null=True, blank=True, related_name='tasks')
    created_by  = ForeignKey(Account, on_delete=SET_NULL, null=True, related_name='created_tasks')
    status      = CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    due_date    = DateField(null=True, blank=True)
    created_at  = DateTimeField(auto_now_add=True)
    updated_at  = DateTimeField(auto_now=True)
```

**Note:** `assigned_to` references `ProjectMember` (not Account directly) to ensure tasks are only assigned to project members.

---

### 7. TaskComment Model (`comments/models.py`)

Comments on tasks with nested reply support.

```python
class TaskComment(Model):
    task            = ForeignKey(Task, on_delete=CASCADE, related_name='comments')
    author          = ForeignKey(Account, on_delete=SET_NULL, null=True, related_name='task_comments')
    parent_comment  = ForeignKey('self', on_delete=CASCADE, null=True, blank=True, related_name='replies')
    content         = TextField()
    created_at      = DateTimeField(auto_now_add=True)
    updated_at      = DateTimeField(auto_now=True)
```

**Self-Referencing Relationship:**
- `parent_comment` allows nested replies
- A comment with `parent_comment = None` is a top-level comment
- Replies reference their parent via `parent_comment`

---

## 🔗 URL Routes

### Root URLs (`workflow_hub/urls.py`)

| Pattern | View | Name | Description |
|---------|------|------|-------------|
| `/` | `views.home` | `home` | Dashboard/home page |
| `/admin/` | Admin site | - | Django admin panel |
| `/accounts/*` | Include accounts.urls | - | Auth routes |
| `/workspace/*` | Include workspaces.urls | - | Workspace routes |
| `/projects/*` | Include projects.urls | - | Project routes |
| `/tasks/*` | Include tasks.urls | - | Task routes |
| `/__debug__/*` | Debug Toolbar | - | Debug toolbar (dev only) |

### Account URLs (`accounts/urls.py`)

| Pattern | View | Name | Description |
|---------|------|------|-------------|
| `/accounts/login/` | `login_view` | `login` | User login |
| `/accounts/register/` | `register_view` | `register` | User registration |
| `/accounts/logout/` | `logout_view` | `logout` | User logout |

### Workspace URLs (`workspaces/urls.py`)

| Pattern | View | Name | Description |
|---------|------|------|-------------|
| `/workspace/` | `workspaces` | `workspaces` | List user's workspaces |
| `/workspace/create/` | `create_workspace` | `create_workspace` | Create new workspace |
| `/workspace/<slug>/` | `workspace_detail` | `workspace_detail` | View workspace details |
| `/workspace/<slug>/add_member/` | `add_member_in_workspace` | `add_member` | Add member to workspace |
| `/workspace/<slug>/create_project/` | `create_workspace_project` | `create_workspace_project` | Create project in workspace |

### Project URLs (`projects/urls.py`)

| Pattern | View | Name | Description |
|---------|------|------|-------------|
| `/projects/` | `projects` | `projects` | Filter projects by workspace |
| `/projects/<ws_slug>/<proj_slug>/` | `project_detail` | `project_detail` | View project details |
| `/projects/<ws_slug>/<proj_slug>/add_new_member` | `add_member` | `add_member` | Add member to project |
| `/projects/<ws_slug>/<proj_slug>/task/*` | Include tasks.urls | - | Task routes (nested) |
| `/projects/<ws_slug>/<proj_slug>/comment/*` | Include comments.urls | - | Comment routes (nested) |

### Task URLs (`tasks/urls.py`)

| Pattern | View | Name | Description |
|---------|------|------|-------------|
| `/tasks/get_all_tasks/` | `get_all_tasks` | `get_all_tasks` | View all user's tasks |
| `/.../task/add_task` | `add_task` | `add_project_task` | Create task (project context) |

### Comment URLs (`comments/urls.py`)

| Pattern | View | Name | Description |
|---------|------|------|-------------|
| `/.../comment/<id>/` | `view_all_comments` | `view_comment_details` | View task comments & add comments |

---

## 🎯 Views & Business Logic

### Authentication Views (`accounts/views.py`)

#### `login_view(request)`
- **GET**: Renders login form (redirects if already authenticated)
- **POST**: Authenticates user with email/password
- Supports `?next=` parameter for redirect after login
- Uses Django's built-in `authenticate()` and `login()`

#### `register_view(request)`
- **GET**: Renders registration form
- **POST**: Creates new user
- Validates: password match, email uniqueness, username uniqueness
- Uses custom `Account.objects.create_user()`

#### `logout_view(request)`
- Logs out user and redirects to login page

---

### Workspace Views (`workspaces/views.py`)

#### `workspaces(request)` - @login_required
Lists all workspaces created by the current user.
- Uses `prefetch_related()` for efficient querying of members and projects
- Counts members and projects for each workspace

#### `create_workspace(request)` - @login_required
- Generates unique slug from workspace name
- Auto-increments slug suffix if duplicate exists (`my-workspace`, `my-workspace-1`, etc.)

#### `workspace_detail(request, slug)` - @login_required
- Displays workspace with members and projects
- Only shows workspaces created by current user

#### `add_member_in_workspace(request, slug)` - @login_required
- Shows available users not already in workspace
- Creates `WorkspaceMember` with selected role

#### `create_workspace_project(request, slug)` - @login_required
- Only workspace members can create projects
- Auto-adds creator as project manager
- Uses `transaction.atomic()` for data integrity

---

### Project Views (`projects/views.py`)

#### `projects(request)` - @login_required
- Displays workspace dropdown filter
- POST request filters projects by selected workspace

#### `project_detail(request, workspace_slug, project_slug)` - @login_required
- Displays project with members and tasks
- Shows task statistics (total, completed, in-progress, todo)
- Uses complex `prefetch_related()` for optimized queries

#### `add_member(request, workspace_slug, project_slug)` - @login_required
- Shows workspace members not yet in project
- Adds selected member with role to `ProjectMember`

---

### Task Views (`tasks/views.py`)

#### `get_all_tasks(request)` - @login_required
Main task dashboard showing:
- **Assigned Tasks**: Tasks where `assigned_to.member == current_user`
- **Created Tasks**: Tasks where `created_by == current_user`
- Grouped by project
- Uses optimized queries with `Prefetch()`

#### `add_task(request, workspace_slug, project_slug)` - @login_required
- Validates user is a project member
- Creates task with title, description, status, assignee, due date
- Validates `assigned_to` is a valid project member

---

### Comment Views (`comments/views.py`)

#### `view_all_comments(request, workspace_slug, project_slug, id)` - @login_required
- Displays all comments and replies for a task
- **POST**: Creates new comment (top-level or reply)
- Uses PRG pattern to prevent duplicate submissions
- Validates parent_comment existence for replies

---

## 📄 Templates

### Template Inheritance Structure

```
base.html (Master Layout)
    │
    ├── home.html (Dashboard)
    │
    ├── accounts/
    │   ├── login.html
    │   └── register.html
    │
    ├── workspaces/
    │   ├── workspaces.html (List)
    │   ├── create_workspace.html
    │   ├── workspace_detail.html
    │   ├── add_member.html
    │   └── create_project.html
    │
    ├── projects/
    │   ├── index.html (List with filter)
    │   ├── project_detail.html
    │   ├── create_project.html
    │   └── add_new_member.html
    │
    ├── tasks/
    │   └── create_task.html
    │
    └── task/
        ├── all_tasks.html (Main task dashboard)
        ├── tast_comments_details.html
        └── comment_item.html (Reusable)
```

### Base Template (`templates/base.html`)

Provides:
- Top navigation bar with app title ("WorkflowHub")
- Collapsible sidebar with navigation links:
  - Dashboard (home)
  - Workspaces
  - Projects
  - Tasks
  - Logout
- Content block for child templates
- Static file includes (CSS, JS)

### Key Template Features

- **Django Template Tags**: `{% extends %}`, `{% block %}`, `{% include %}`, `{% url %}`, `{% static %}`
- **Template Filters**: `|slice`, `|truncatewords`, `|date`, `|length`
- **Conditional Rendering**: `{% if %}`, `{% for %}`, `{% empty %}`
- **Status Badge System**: Dynamic classes based on task status

---

## 🔐 Authentication System

### Configuration (`settings.py`)

```python
AUTH_USER_MODEL = 'accounts.Account'  # Custom user model

LOGIN_URL = 'login'                    # Redirect here if @login_required fails
LOGIN_REDIRECT_URL = 'home'            # Redirect here after login
LOGOUT_REDIRECT_URL = 'login'          # Redirect here after logout
```

### Protection Mechanism

All views except login/register are protected with `@login_required`:

```python
from django.contrib.auth.decorators import login_required

@login_required
def some_view(request):
    # Only authenticated users reach here
    pass
```

### Authentication Flow

```
                    ┌─────────────────┐
                    │  Unauthenticated│
                    │      User       │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
    ┌─────────────────┐          ┌─────────────────┐
    │    /login/      │          │   /register/    │
    │                 │          │                 │
    │ Email + Password│          │ Create Account  │
    └────────┬────────┘          └────────┬────────┘
             │                            │
             │                            │
             ▼                            ▼
    ┌─────────────────┐          ┌─────────────────┐
    │   authenticate  │          │  create_user()  │
    │   + login()     │          │  + redirect     │
    └────────┬────────┘          └─────────────────┘
             │
             ▼
    ┌─────────────────┐
    │   Authenticated │
    │     Session     │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │  Access Protected│
    │      Views       │
    └─────────────────┘
```

---

## 🚀 Installation Guide

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Git (optional, for cloning)

### Step-by-Step Installation

#### 1. Clone or Download the Project

```bash
git clone https://github.com/yourusername/workflow_management_system.git
cd workflow_management_system
```

#### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv env
env\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv env
source env/bin/activate
```

#### 3. Install Dependencies

```bash
pip install django django-debug-toolbar
```

Or if you have a requirements.txt:
```bash
pip install -r requirements.txt
```

#### 4. Apply Database Migrations

```bash
python manage.py migrate
```

This creates all necessary database tables.

#### 5. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

You'll be prompted for:
- Email (used for login)
- Username
- First name
- Last name
- Password

#### 6. Run Development Server

```bash
python manage.py runserver
```

#### 7. Access the Application

- **Application**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Debug Toolbar**: Visible in DEBUG mode on the right side

---

## ⚙️ Configuration

### Key Settings (`workflow_hub/settings.py`)

```python
# Security (Change in Production!)
SECRET_KEY = 'your-secret-key-here'
DEBUG = True  # Set False in production
ALLOWED_HOSTS = []  # Add your domain in production

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static Files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Auth
AUTH_USER_MODEL = 'accounts.Account'
LOGIN_URL = 'login'
```

### Installed Apps

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',      # Custom user auth
    'comments',      # Task comments
    'projects',      # Project management
    'tasks',         # Task management
    'workspaces',    # Workspace management
    'debug_toolbar', # Development debugging
]
```

---

## 📖 Usage Guide

### 1. Getting Started

1. Register a new account at `/accounts/register/`
2. Login with your email and password
3. You'll be redirected to the dashboard

### 2. Creating Your First Workspace

1. Go to **Workspaces** from the sidebar
2. Click **Create Workspace**
3. Enter workspace name and status
4. Your workspace is ready!

### 3. Adding Team Members

1. Open a workspace
2. Click **Add Member**
3. Select a user and assign a role (Manager, Leader, Developer, etc.)
4. Member is now part of the workspace

### 4. Creating a Project

1. Open a workspace
2. Click **Create Project**
3. Enter project name and status
4. You're automatically added as project manager

### 5. Managing Tasks

1. Open a project
2. Click **Add Task**
3. Fill in:
   - Title (required)
   - Description
   - Status (To Do, In Progress, Review, Completed)
   - Assignee (from project members)
   - Due date
4. View all your tasks at `/tasks/get_all_tasks/`

### 6. Commenting on Tasks

1. Open a project
2. Click on a task to view comments
3. Add top-level comments or reply to existing comments
4. Comments support threaded discussions

---

## 🎨 CSS Theme Variables

The application uses CSS Custom Properties for easy theming:

```css
:root {
    /* Brand Colors */
    --primary: #4F46E5;
    --primary-hover: #4338CA;
    
    /* Text Colors */
    --text-heading: #1F2937;
    --text-body: #4B5563;
    --text-muted: #9CA3AF;
    
    /* Backgrounds */
    --bg-main: #F9FAFB;
    --bg-card: #FFFFFF;
    --bg-sidebar: #1F2937;
    
    /* Borders */
    --border-color: #E5E7EB;
    
    /* Status Colors */
    --success: #16A34A;
    --in-progress: #3B82F6;
    --review: #F59E0B;
    --danger: #DC2626;
}
```

---

## 🔜 Roadmap / Future Features

- [ ] REST API with Django REST Framework
- [ ] Email notifications for task assignments
- [ ] File attachments on tasks
- [ ] Activity/audit logs
- [ ] Dashboard analytics & charts
- [ ] Task drag-and-drop kanban board
- [ ] Real-time updates with WebSockets
- [ ] Export tasks to CSV/PDF
- [ ] Calendar view for due dates
- [ ] Search and filter functionality

---

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep views thin, move business logic to models or utilities

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

Built with ❤️ using Django

---

⭐ **If you found this project helpful, please give it a star!**
