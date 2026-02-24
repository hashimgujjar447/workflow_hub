# WorkflowHub 🚀

A robust team workflow management system built with Django 6.0. WorkflowHub helps teams organize work using a hierarchy: **Workspaces → Projects → Tasks**, featuring secure authentication, role-based access, and threaded comments.

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
- **Modern UI:** Responsive design, CSS variables, sidebar navigation, status badges

---

## 🛠️ Tech Stack

| Category            | Technology                  |
|---------------------|----------------------------|
| Backend Framework   | Django 6.0.1               |
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
│
├── tasks (work items)
└── comments (discussions)
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
WorkspaceMember ProjectMember TaskComment (self-referencing for replies)
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
        ROLE_CHOICES = (...)  # Same as WorkspaceMember
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

- **Root URLs:** `/`, `/admin/`, `/accounts/*`, `/workspace/*`, `/projects/*`, `/tasks/*`, `/__debug__/*`
- **Accounts:** `/accounts/login/`, `/accounts/register/`, `/accounts/logout/`
- **Workspaces:** `/workspace/`, `/workspace/create/`, `/workspace/<slug>/`, `/workspace/<slug>/add_member/`, `/workspace/<slug>/create_project/`
- **Projects:** `/projects/`, `/projects/<ws_slug>/<proj_slug>/`, `/projects/<ws_slug>/<proj_slug>/add_new_member`, `/projects/<ws_slug>/<proj_slug>/task/*`, `/projects/<ws_slug>/<proj_slug>/comment/*`
- **Tasks:** `/tasks/get_all_tasks/`, `/.../task/add_task`
- **Comments:** `/.../comment/<id>/`

---

## 🎯 Views & Business Logic

- **Authentication:** Login, register, logout views; email/password authentication
- **Workspace:** List, create, detail, add member, create project
- **Project:** List, detail, add member
- **Task:** Dashboard, create task
- **Comment:** View/add comments, threaded replies

---

## 📄 Templates

- **base.html:** Master layout, sidebar, navigation
- **home.html:** Dashboard
- **accounts:** Login/register templates
- **workspaces:** List, create, detail, add member, create project
- **projects:** List, detail, create, add member
- **tasks:** Create task
- **task:** Task dashboard, comments, reusable fragments

---

## 🔐 Authentication System

- Custom user model (`AUTH_USER_MODEL = 'accounts.Account'`)
- All views protected with `@login_required`
- Login/logout redirects configured in `settings.py`

---

## 🚀 Installation Guide

1. **Clone:** `git clone https://github.com/yourusername/workflow_management_system.git`
2. **Virtual Env:** `python -m venv env` & activate
3. **Install:** `pip install django django-debug-toolbar`
4. **Migrate:** `python manage.py migrate`
5. **Superuser:** `python manage.py createsuperuser`
6. **Run:** `python manage.py runserver`
7. **Access:** http://127.0.0.1:8000/

---

## ⚙️ Configuration

- `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `DATABASES`, `STATIC_URL`, `AUTH_USER_MODEL`, `LOGIN_URL`
- Installed apps: accounts, comments, projects, tasks, workspaces, debug_toolbar

---

## 📖 Usage Guide

1. Register at `/accounts/register/`
2. Login
3. Create workspace
4. Add members
5. Create project
6. Add tasks
7. Comment on tasks

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

- REST API
- Email notifications
- File attachments
- Audit logs
- Analytics & charts
- Kanban board
- Real-time updates
- Export tasks
- Calendar view
- Search/filter

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
