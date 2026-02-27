# WorkflowHub 🚀

A robust team workflow management system built with **Django 6.0.1**. WorkflowHub helps teams organize work using a clear hierarchy:

```
Workspace → Project → Task → Comment
```

It features secure email-based authentication, role-based access control, threaded comments, a full HTML web UI, and a complete REST API with JWT support.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Django](https://img.shields.io/badge/Django-6.0.1-green)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791)
![DRF](https://img.shields.io/badge/API-Django%20REST%20Framework-red)
![JWT](https://img.shields.io/badge/Auth-JWT%20%2B%20Session-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📑 Table of Contents

1. [Overview](#-overview)
2. [Features](#-features)
3. [Tech Stack](#-tech-stack)
4. [Project Structure](#-project-structure)
5. [Application Architecture](#-application-architecture)
6. [Database Models](#-database-models)
7. [Role System](#-role-system)
8. [URL Routes](#-url-routes)
9. [Views & Business Logic](#-views--business-logic)
10. [REST API](#-rest-api)
11. [Serializers](#-serializers)
12. [Permissions](#-permissions)
13. [Installation Guide](#-installation-guide)
14. [Configuration](#-configuration)
15. [Usage Guide](#-usage-guide)
16. [Roadmap](#-roadmap)

---

## 🧭 Overview

WorkflowHub is a full-stack Django project management platform. It has two layers:

- **Web UI** — Traditional Django template-based views for browser usage
- **REST API** — Full DRF-based API with JWT authentication for client/mobile apps

### Data Hierarchy

```
Account (User)
 └── Workspace
      ├── WorkspaceMember (role: manager/leader/frontend/backend/seo)
      └── Project
           ├── ProjectMember (same role set)
           └── Task
                └── TaskComment (supports nested replies)
```

---

## 📋 Features

- **Custom Auth:** Email-based login using `AbstractBaseUser`, custom `AccountManager`
- **Workspace Management:** Create workspaces, auto-generate unique slugs, invite members with roles
- **Project Management:** Projects inside workspaces, status tracking, role-based creation
- **Task Management:** Assign tasks to project members, set status & due date
- **Threaded Comments:** Nested replies using self-referential FK on `TaskComment`
- **Soft Delete:** Workspaces and Projects are deactivated (`is_active=False`), not hard deleted
- **REST API:** Full CRUD API with JWT + Session auth, nested URL structure
- **Role-based Permissions:** Custom `IsManager` permission restricts sensitive operations
- **Debug Toolbar:** Integrated `django-debug-toolbar` for development
- **Admin Panel:** Customized admin for all models

---

## 🛠️ Tech Stack

| Category            | Technology                          |
|---------------------|-------------------------------------|
| Backend Framework   | Django 6.0.1                        |
| API Framework       | Django REST Framework               |
| Authentication      | JWT (simplejwt) + Session           |
| Database            | PostgreSQL                          |
| Frontend            | HTML5, CSS3, Vanilla JavaScript     |
| Debug Tools         | Django Debug Toolbar                |
| Python Version      | Python 3.x                          |

### Dependencies

```
asgiref==3.11.0
Django==6.0.1
django-debug-toolbar==6.2.0
djangorestframework==3.16.1
djangorestframework_simplejwt==5.5.1
psycopg2-binary==2.9.11
PyJWT==2.11.0
pyparsing==3.3.2
sqlparse==0.5.5
tzdata==2025.3
```

---

## 📁 Project Structure

```
workflow_management_system/
│
├── manage.py
├── db.sqlite3
├── api.http                          # HTTP test file for API
├── README.md
│
├── workflow_hub/                     # Main Django project config
│   ├── settings.py
│   ├── urls.py                       # Root URL config
│   ├── views.py                      # Home view
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/                         # Custom user auth
│   ├── models.py                     # Account, AccountManager
│   ├── views.py                      # login, register, logout, profile
│   ├── urls.py
│   └── admin.py                      # Custom AccountAdmin
│
├── workspaces/                       # Workspace management
│   ├── models.py                     # Workspace, WorkspaceMember
│   ├── views.py                      # CRUD + member management
│   ├── urls.py
│   └── admin.py
│
├── projects/                         # Project management
│   ├── models.py                     # Project, ProjectMember
│   ├── views.py                      # CRUD + member management
│   ├── urls.py
│   └── admin.py
│
├── tasks/                            # Task management
│   ├── models.py                     # Task
│   ├── views.py                      # get_all_tasks, add_task
│   ├── urls.py
│   └── admin.py
│
├── comments/                         # Threaded comments
│   ├── models.py                     # TaskComment (self-FK for replies)
│   ├── views.py                      # view_all_comments (GET + POST)
│   ├── urls.py
│   └── admin.py
│
├── api/                              # REST API layer
│   ├── urls.py                       # All API routes
│   ├── permissions.py                # IsManager custom permission
│   ├── serializers/
│   │   ├── common_serializers.py     # UserSerializer
│   │   ├── workspace.py              # WorkspaceSerializer
│   │   ├── workspace_members.py      # WorkSpaceMemberSerializer
│   │   ├── workspace_projects.py     # Project + ProjectMember serializers
│   │   ├── task_serializers.py       # ProjectTaskSerializer
│   │   ├── comment_serializer.py     # CommentSerializer + CommentPagination
│   │   └── comment_reply_serializer.py  # CommentDetailSerializer (recursive)
│   └── views/
│       ├── workspace.py              # ListCreate + Detail workspace views
│       ├── workspace_members.py      # ListCreate workspace members
│       ├── workspace_projects.py     # Projects + Tasks list views
│       ├── project_task_details.py   # Retrieve/Update/Delete task
│       └── task_comments.py          # Paginated threaded comments
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── 403.html
│   ├── accounts/
│   │   ├── login.html
│   │   ├── register.html
│   │   └── profile.html
│   ├── workspaces/
│   │   ├── workspaces.html
│   │   ├── create_workspace.html
│   │   ├── workspace_detail.html
│   │   ├── add_member.html
│   │   ├── create_project.html
│   │   └── settings.html
│   ├── projects/
│   │   ├── index.html
│   │   ├── project_detail.html
│   │   ├── create_project.html
│   │   ├── add_new_member.html
│   │   └── settings.html
│   ├── tasks/
│   │   └── create_task.html
│   ├── task/
│   │   ├── all_tasks.html
│   │   ├── tast_comments_details.html
│   │   └── comment_item.html
│   └── includes/
│       ├── header.html
│       └── footer.html
│
├── static/
│   ├── css/style.css
│   └── js/index.js
│
└── env/                              # Virtual environment
```

---

## 🏛️ Application Architecture

### Request Flow — Web UI

```
HTTP Request
    │
    ▼
URL Router (workflow_hub/urls.py)
    │
    ▼
@login_required Decorator
    │
    ▼
View Function
    │
    ▼
ORM Queries (Models)
    │
    ▼
Template Render → HTTP Response
```

### Request Flow — REST API

```
HTTP Request
    │
    ▼
URL Router (/api/...)
    │
    ▼
JWT / Session Authentication
    │
    ▼
IsAuthenticated + IsManager (if needed)
    │
    ▼
APIView / GenericAPIView
    │
    ▼
Serializer (validate + serialize)
    │
    ▼
ORM Queries → JSON Response
```

---

## 🗃️ Database Models

### Entity Relationship

```
Account
 ├── Workspace (created_workspaces)
 │     ├── WorkspaceMember ←── Account
 │     └── Project (created_by → Account)
 │           ├── ProjectMember ←── Account
 │           └── Task
 │                 ├── assigned_to → ProjectMember
 │                 ├── created_by → Account
 │                 └── TaskComment
 │                       └── parent_comment → TaskComment (self-ref)
```

---

### 1. `Account` — `accounts/models.py`

| Field          | Type            | Notes                              |
|----------------|-----------------|------------------------------------|
| `first_name`   | CharField(50)   |                                    |
| `last_name`    | CharField(50)   |                                    |
| `username`     | CharField(100)  | unique                             |
| `email`        | EmailField(100) | unique · `USERNAME_FIELD`          |
| `phone_number` | CharField(50)   | optional                           |
| `date_joined`  | DateTimeField   | auto_now_add                       |
| `last_login`   | DateTimeField   | auto_now                           |
| `is_admin`     | BooleanField    | default False                      |
| `is_staff`     | BooleanField    | default False                      |
| `is_active`    | BooleanField    | default True                       |
| `is_superadmin`| BooleanField    | default False                      |

`USERNAME_FIELD = 'email'` · `REQUIRED_FIELDS = ['username', 'first_name', 'last_name']`

---

### 2. `Workspace` — `workspaces/models.py`

| Field        | Type           | Notes                            |
|--------------|----------------|----------------------------------|
| `name`       | CharField(100) |                                  |
| `slug`       | SlugField(100) | unique · auto-generated on save  |
| `creator`    | FK → Account   | related_name=`created_workspaces`|
| `is_active`  | BooleanField   | default True · soft delete       |
| `created_at` | DateTimeField  | auto_now_add                     |
| `updated_at` | DateTimeField  | auto_now                         |

> **Auto-slug logic:** On save, slug generated from `name`. If collision exists, appends `-1`, `-2`, etc.

---

### 3. `WorkspaceMember` — `workspaces/models.py`

| Field       | Type           | Notes                               |
|-------------|----------------|-------------------------------------|
| `workspace` | FK → Workspace | related_name=`members`              |
| `user`      | FK → Account   | related_name=`workspace_memberships`|
| `role`      | CharField(20)  | choices — see Role System           |
| `joined_at` | DateTimeField  | auto_now_add                        |
| `is_active` | BooleanField   | default True                        |

`unique_together = ('workspace', 'user')`

---

### 4. `Project` — `projects/models.py`

| Field        | Type           | Notes                                     |
|--------------|----------------|-------------------------------------------|
| `workspace`  | FK → Workspace | related_name=`projects`                   |
| `name`       | CharField(150) |                                           |
| `slug`       | SlugField(150) | auto-generated                            |
| `status`     | CharField(20)  | pending / in_progress / completed / failed|
| `created_by` | FK → Account   | SET_NULL · null=True                      |
| `is_active`  | BooleanField   | default True · soft delete                |
| `created_at` | DateTimeField  | auto_now_add                              |
| `updated_at` | DateTimeField  | auto_now                                  |

`unique_together = ('workspace', 'slug')` · `ordering = ['-created_at']`

---

### 5. `ProjectMember` — `projects/models.py`

| Field       | Type          | Notes                               |
|-------------|---------------|-------------------------------------|
| `member`    | FK → Account  | related_name=`project_memberships`  |
| `project`   | FK → Project  | related_name=`members`              |
| `role`      | CharField(50) | choices — see Role System           |
| `is_active` | BooleanField  | default True                        |
| `joined_at` | DateTimeField | auto_now_add                        |
| `updated_at`| DateTimeField | auto_now                            |

`unique_together = ('project', 'member')`

---

### 6. `Task` — `tasks/models.py`

| Field         | Type               | Notes                                          |
|---------------|--------------------|------------------------------------------------|
| `project`     | FK → Project       | related_name=`tasks`                           |
| `title`       | CharField(200)     |                                                |
| `description` | TextField          | blank=True                                     |
| `assigned_to` | FK → ProjectMember | SET_NULL · null=True · blank=True              |
| `created_by`  | FK → Account       | SET_NULL · null=True                           |
| `status`      | CharField(20)      | todo / in_progress / review / completed / failed|
| `due_date`    | DateField          | null=True · blank=True                         |
| `created_at`  | DateTimeField      | auto_now_add                                   |
| `updated_at`  | DateTimeField      | auto_now                                       |

---

### 7. `TaskComment` — `comments/models.py`

| Field            | Type           | Notes                                       |
|------------------|----------------|---------------------------------------------|
| `task`           | FK → Task      | related_name=`comments`                     |
| `author`         | FK → Account   | SET_NULL · null=True                        |
| `parent_comment` | FK → self      | null=True · blank=True · related_name=`replies` |
| `content`        | TextField      |                                             |

> Top-level comments: `parent_comment=None`. Replies: point to parent. Recursively nested via `replies`.

---

## 👥 Role System

Both `WorkspaceMember` and `ProjectMember` use the same roles:

| Role       | Label               | Can Create Project | Can Add Members (API) |
|------------|---------------------|--------------------|------------------------|
| `manager`  | Manager             | ✅                 | ✅                     |
| `leader`   | Leader              | ✅                 | ❌                     |
| `frontend` | Frontend Developer  | ❌                 | ❌                     |
| `backend`  | Backend Developer   | ❌                 | ❌                     |
| `seo`      | SEO                 | ❌                 | ❌                     |

- Workspace **creator** is auto-added as `manager` on workspace creation
- Project **creator** is auto-added as `manager` via `get_or_create`

---

## 🔗 URL Routes

### Web Application

| URL                                                   | View                       | Name                        |
|-------------------------------------------------------|----------------------------|-----------------------------|
| `/`                                                   | `home`                     | `home`                      |
| `/accounts/login/`                                    | `login_view`               | `login`                     |
| `/accounts/register/`                                 | `register_view`            | `register`                  |
| `/accounts/logout/`                                   | `logout_view`              | `logout`                    |
| `/accounts/profile/`                                  | `profile_view`             | `profile`                   |
| `/workspace/`                                         | `workspaces`               | `workspaces`                |
| `/workspace/create/`                                  | `create_workspace`         | `create_workspace`          |
| `/workspace/<slug>/`                                  | `workspace_detail`         | `workspace_detail`          |
| `/workspace/<slug>/add_member/`                       | `add_member_in_workspace`  | `add_member`                |
| `/workspace/<slug>/create_project/`                   | `create_workspace_project` | `create_workspace_project`  |
| `/workspace/<slug>/settings/`                         | `workspace_settings`       | `workspace_settings`        |
| `/projects/`                                          | `projects`                 | `projects`                  |
| `/projects/<ws_slug>/<proj_slug>/`                    | `project_detail`           | `project_detail`            |
| `/projects/<ws_slug>/<proj_slug>/add_new_member`      | `add_member`               | `add_member`                |
| `/projects/<ws_slug>/<proj_slug>/settings/`           | `project_settings`         | `project_settings`          |
| `/projects/<ws_slug>/<proj_slug>/task/add_task`       | `add_task`                 | `add_project_task`          |
| `/tasks/get_all_tasks/`                               | `get_all_tasks`            | `get_all_tasks`             |
| `/projects/<ws_slug>/<proj_slug>/comment/<id>/`       | `view_all_comments`        | `view_comment_details`      |

### REST API

| Method        | Endpoint                                                           | Description                      | Permission       |
|---------------|--------------------------------------------------------------------|----------------------------------|------------------|
| `POST`        | `/api/token/`                                                      | Obtain JWT tokens                | Public           |
| `POST`        | `/api/token/refresh/`                                              | Refresh access token             | Public           |
| `GET`         | `/api/workspaces/`                                                 | List user workspaces             | IsAuthenticated  |
| `POST`        | `/api/workspaces/`                                                 | Create workspace                 | IsAuthenticated  |
| `GET`         | `/api/workspaces/<slug>/`                                          | Workspace detail                 | IsAuthenticated  |
| `PUT/PATCH`   | `/api/workspaces/<slug>/`                                          | Update workspace                 | IsAuthenticated  |
| `DELETE`      | `/api/workspaces/<slug>/`                                          | Delete workspace                 | IsAuthenticated  |
| `GET`         | `/api/workspaces/<slug>/members/`                                  | List members                     | IsAuthenticated  |
| `POST`        | `/api/workspaces/<slug>/members/`                                  | Add member                       | IsManager        |
| `GET`         | `/api/workspaces/<slug>/projects/`                                 | List projects                    | IsAuthenticated  |
| `POST`        | `/api/workspaces/<slug>/projects/`                                 | Create project                   | IsAuthenticated  |
| `GET`         | `/api/workspaces/<slug>/projects/<proj_slug>/`                     | Project detail (with members)    | IsAuthenticated  |
| `PUT/PATCH`   | `/api/workspaces/<slug>/projects/<proj_slug>/`                     | Update project                   | IsAuthenticated  |
| `DELETE`      | `/api/workspaces/<slug>/projects/<proj_slug>/`                     | Delete project                   | IsAuthenticated  |
| `GET`         | `/api/workspaces/<slug>/projects/<proj_slug>/tasks/`               | List tasks                       | IsAuthenticated  |
| `GET/PUT/DEL` | `/api/workspaces/<slug>/projects/<proj_slug>/tasks/<id>/`          | Task detail/update/delete        | IsAuthenticated  |
| `GET`         | `/api/workspaces/<slug>/projects/<proj_slug>/tasks/<id>/comments/` | Paginated threaded comments      | IsAuthenticated  |
| `POST`        | `/api/workspaces/<slug>/projects/<proj_slug>/tasks/<id>/comments/` | Add comment/reply                | IsAuthenticated  |

---

## 🎯 Views & Business Logic

### `accounts/views.py`

| View            | Logic                                                                  |
|-----------------|------------------------------------------------------------------------|
| `login_view`    | Email+password auth, redirect to `next` param or `home`               |
| `register_view` | Validates duplicate email/username, creates `Account` via manager      |
| `logout_view`   | Calls `logout()`, redirects to login                                   |
| `profile_view`  | Shows count of created workspaces + workspace memberships              |

### `workspaces/views.py`

| View                       | Logic                                                                |
|----------------------------|----------------------------------------------------------------------|
| `workspaces`               | Q filter: `creator=user OR members__user=user`, distinct            |
| `create_workspace`         | Creates workspace + auto-adds creator as `manager`                  |
| `workspace_detail`         | Members, projects, stats; checks creator/manager flags               |
| `add_member_in_workspace`  | Excludes existing members from available list, prevents duplicates   |
| `create_workspace_project` | Only manager/leader can create; `transaction.atomic()`; auto-adds creator as project manager |
| `workspace_settings`       | Only manager can soft-delete (`is_active=False`)                    |

### `projects/views.py`

| View               | Logic                                                                        |
|--------------------|------------------------------------------------------------------------------|
| `projects`         | Lists workspaces; filters projects by selected workspace (POST)              |
| `project_detail`   | Prefetches tasks+comments+replies; shows task stats (todo/in_progress/completed) |
| `add_member`       | Compares workspace members vs project members; adds only non-members         |
| `project_settings` | Only manager/leader can soft-delete project                                  |

### `tasks/views.py`

| View            | Logic                                                                      |
|-----------------|----------------------------------------------------------------------------|
| `get_all_tasks` | Groups tasks by project; separates assigned vs created tasks for current user |
| `add_task`      | Validates project membership; creates task with optional assignment & due date |

### `comments/views.py`

| View                | Logic                                                                  |
|---------------------|------------------------------------------------------------------------|
| `view_all_comments` | GET: renders threaded comments. POST: validates task_id match, creates comment or reply |

---

## 🌐 REST API Views

| View Class                         | Base Class                     | Purpose                              |
|------------------------------------|--------------------------------|--------------------------------------|
| `ListCreateWorkspaceView`          | `ListCreateAPIView`            | List (annotated) + create workspaces |
| `WorkSpaceDetailView`              | `RetrieveUpdateDestroyAPIView` | Workspace CRUD by slug               |
| `ListCreateWorkspaceMembersApiView`| `ListCreateAPIView`            | Members list + add (IsManager on POST)|
| `WorkspaceProjectApiView`          | `ListCreateAPIView`            | Project list + create                |
| `WorkspaceProjectDetailsApiView`   | `RetrieveUpdateDestroyAPIView` | Project detail/update/delete         |
| `ProjectTasksApiView`              | `ListAPIView`                  | Task list for a project              |
| `RetrieveTaskApiView`              | `RetrieveUpdateDestroyAPIView` | Task detail/update/delete            |
| `TaskCommentsAPIView`              | `ListCreateAPIView`            | Paginated threaded comments          |

### Query Optimizations in API

- Workspaces annotated with `total_members`, `total_projects` (single query, no extra hits)
- `select_related` and `prefetch_related` used throughout all views
- Workspace list: `Q(creator=user) | Q(members__user=user)` with `.distinct()`
- `TaskCommentsAPIView` prefetches `replies__author` in one query

---

## 📦 Serializers

| Serializer                         | Model           | Key Fields                                              |
|------------------------------------|-----------------|----------------------------------------------------------|
| `UserSerializer`                   | Account         | first_name, last_name, email, username, date_joined      |
| `WorkspaceSerializer`              | Workspace       | name, slug, creator, is_active, total_members*, total_projects* |
| `WorkSpaceMemberSerializer`        | WorkspaceMember | user, role, joined_at, is_active                         |
| `WorkspaceProjectSerializer`       | Project         | name, slug, status, is_active, created_at                |
| `WorkspaceProjectDetailSerializer` | Project         | name, slug, members (nested), total_members*, created_by |
| `WorkSpaceProjectMembersSerializer`| ProjectMember   | member (UserSerializer), role, is_active, joined_at      |
| `ProjectTaskSerializer`            | Task            | title, description, assigned_to, created_by, status, due_date, comments |
| `CommentSerializer`                | TaskComment     | author, content, created_at, parent_comment — **POST only** |
| `CommentDetailSerializer`          | TaskComment     | id, content, author, replies (recursive) — **GET only**  |

`*` = annotated field (not a DB column, injected via `.annotate()`)

### Comment Pagination
```python
class CommentPagination(PageNumberPagination):
    page_size = 5
```

`TaskCommentsAPIView` automatically uses `CommentSerializer` for POST and `CommentDetailSerializer` for GET via `get_serializer_class()`.

---

## 🔐 Permissions

### Web UI
- All views protected with `@login_required`
- Role checks done inline (e.g., `project.members.filter(role__in=['manager','leader'])`)
- `PermissionDenied` raised for unauthorized actions

### REST API — Custom `IsManager` Permission

```python
# api/permissions.py
class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method != "POST":
            return True   # GET always allowed
        workspace_slug = view.kwargs.get("workspace_slug")
        member = WorkspaceMember.objects.get(
            workspace__slug=workspace_slug,
            user=request.user,
            is_active=True
        )
        return member.role in ['manager']
```

Applied to `ListCreateWorkspaceMembersApiView` — only managers can `POST` (add members).

### Global API Auth Settings

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

## 🚀 Installation Guide

### Prerequisites
- Python 3.x
- PostgreSQL installed and running

### Steps

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/workflow_management_system.git
cd workflow_management_system
```

**2. Create and activate virtual environment**
```bash
python -m venv env

# Windows
env\Scripts\activate

# macOS/Linux
source env/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up PostgreSQL database**
```sql
CREATE DATABASE workflow_db;
```

**5. Configure database in `workflow_hub/settings.py`**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'workflow_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

**6. Run migrations**
```bash
python manage.py migrate
```

**7. Create superuser**
```bash
python manage.py createsuperuser
```

**8. Run development server**
```bash
python manage.py runserver
```

**9. Access the app**

| URL                              | Description           |
|----------------------------------|-----------------------|
| http://127.0.0.1:8000/           | Web App Home          |
| http://127.0.0.1:8000/admin/     | Django Admin Panel    |
| http://127.0.0.1:8000/api/       | REST API Root         |
| http://127.0.0.1:8000/__debug__/ | Debug Toolbar         |

---

## ⚙️ Configuration

### Key Settings (`workflow_hub/settings.py`)

| Setting                | Value                            | Purpose                        |
|------------------------|----------------------------------|--------------------------------|
| `AUTH_USER_MODEL`      | `'accounts.Account'`             | Custom user model              |
| `LOGIN_URL`            | `'login'`                        | Redirect for unauthenticated   |
| `LOGIN_REDIRECT_URL`   | `'home'`                         | After successful login         |
| `LOGOUT_REDIRECT_URL`  | `'login'`                        | After logout                   |
| `DEBUG`                | `True`                           | Dev mode (disable in prod)     |
| `INTERNAL_IPS`         | `["127.0.0.1"]`                  | Debug toolbar                  |
| `STATIC_URL`           | `'/static/'`                     | Static files URL               |
| `STATICFILES_DIRS`     | `[BASE_DIR / 'static']`          | Static files location          |
| `STATIC_ROOT`          | `BASE_DIR / 'staticfiles'`       | Collected static (prod)        |
| `CSRF_TRUSTED_ORIGINS` | localhost:8000, 127.0.0.1:8000   | CSRF whitelisted origins       |

---

## 📖 Usage Guide

### Web App Workflow

1. **Register** at `/accounts/register/`
2. **Login** at `/accounts/login/` using email & password
3. **Create Workspace** — you are auto-assigned as `manager`
4. **Add Members** — assign roles (manager / leader / frontend / backend / seo)
5. **Create Project** — only manager or leader can create
6. **Add Project Members** — from existing workspace members
7. **Create Tasks** — assign to project members, set status & due date
8. **Track Tasks** — view all assigned/created tasks at `/tasks/get_all_tasks/`
9. **Comment** — add threaded comments/replies on tasks
10. **Settings** — soft-delete projects or workspaces (manager only)

### REST API Usage

**Obtain JWT token**
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "yourpassword"}'
```

Response:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1Qi..."
}
```

**List workspaces**
```bash
curl http://127.0.0.1:8000/api/workspaces/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Create workspace**
```bash
curl -X POST http://127.0.0.1:8000/api/workspaces/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Team Workspace"}'
```

**Add member to workspace (manager only)**
```bash
curl -X POST http://127.0.0.1:8000/api/workspaces/my-workspace/members/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user": 2, "role": "backend"}'
```

**Add comment to task**
```bash
curl -X POST http://127.0.0.1:8000/api/workspaces/my-ws/projects/my-proj/tasks/1/comments/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "Looks good!", "parent_comment": null}'
```

**Refresh token**
```bash
curl -X POST http://127.0.0.1:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "YOUR_REFRESH_TOKEN"}'
```

### API Response Codes

| Code  | Meaning                     |
|-------|-----------------------------|
| `200` | OK — successful GET/PUT     |
| `201` | Created — successful POST   |
| `204` | No Content — DELETE success |
| `400` | Bad Request — validation    |
| `401` | Unauthorized — no/bad token |
| `403` | Forbidden — no permission   |
| `404` | Not Found                   |

---

## � Production Deployment

> ⚠️ **The project is NOT production-ready in its current state.** The following changes are required before hosting.

### ❌ What Must Be Fixed Before Hosting

| Issue | Current Value | Required Fix |
|---|---|---|
| `DEBUG` | `True` | Set to `False` |
| `SECRET_KEY` | Hardcoded insecure key | Use environment variable |
| `ALLOWED_HOSTS` | `[]` (empty) | Add your domain e.g. `['yourdomain.com']` |
| DB credentials | Hardcoded in settings | Move to environment variables |
| `CSRF_TRUSTED_ORIGINS` | localhost only | Add production domain |
| `debug_toolbar` | Always loaded | Disable in production |
| Static files | Not collected | Run `collectstatic` |
| WSGI server | Dev server | Use `gunicorn` |

### ✅ Step-by-Step Production Checklist

**1. Install production dependencies**
```bash
pip install gunicorn
pip install whitenoise
pip install python-decouple   # for .env file support
```

**2. Create a `.env` file in project root**
```env
SECRET_KEY=your-very-long-random-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_NAME=workflow_db
DB_USER=postgres
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

**3. Update `settings.py` for production**
```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Whitenoise for static files
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add after SecurityMiddleware
    # ... rest of middleware
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Remove debug_toolbar from INSTALLED_APPS and MIDDLEWARE in production
```

**4. Collect static files**
```bash
python manage.py collectstatic --noinput
```

**5. Run database migrations**
```bash
python manage.py migrate
```

**6. Start with Gunicorn**
```bash
gunicorn workflow_hub.wsgi:application --bind 0.0.0.0:8000
```

### 🌐 Hosting Platforms

| Platform | Notes |
|---|---|
| **Railway** | Easy PostgreSQL + Django deploy, supports `requirements.txt` |
| **Render** | Free tier available, add `gunicorn` start command |
| **Heroku** | Needs `Procfile`: `web: gunicorn workflow_hub.wsgi` |
| **DigitalOcean App Platform** | Good for production, supports env vars |
| **VPS (Ubuntu)** | Full control — use Nginx + Gunicorn + systemd |

---

## �🔜 Roadmap

- [x] Custom user authentication (email-based)
- [x] Workspace management with role system
- [x] Project management with member roles
- [x] Task assignment with status & due date
- [x] Threaded comments with nested replies
- [x] REST API with JWT + Session auth
- [x] Soft delete for workspaces and projects
- [x] Custom `IsManager`, `IsManagerOrLeader`, `IsProjectMember` permissions
- [x] Django Debug Toolbar integration
- [x] Fixed: `comment.author` field used correctly across templates
- [x] Fixed: Role values matched to `ROLE_CHOICES` in add member forms
- [x] Fixed: `is_allow_to_delete_and_create` returns proper boolean
- [x] Fixed: Workspace detail access-gated to members only
- [x] Fixed: Workspace `add_member` requires manager/creator permission
- [x] Fixed: Hardcoded URLs replaced with `{% url %}` tags
- [ ] `requirements.txt` added ✅ (done)
- [ ] Production environment setup (`.env`, gunicorn, whitenoise)
- [ ] Email notifications on task assignment
- [ ] File attachments on tasks
- [ ] Real-time updates (Django Channels / WebSockets)
- [ ] Kanban board view
- [ ] Analytics dashboard (charts, stats)
- [ ] Export tasks to PDF / CSV
- [ ] Task dependencies
- [ ] Time tracking per task
- [ ] Advanced search & filtering
- [ ] Audit logs / activity feed

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit: `git commit -m "Add your feature"`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

**Code Guidelines:**
- Follow PEP 8
- Keep views thin — logic in models/services
- Use `select_related` / `prefetch_related` to avoid N+1 queries
- All views must have `@login_required` or `IsAuthenticated`

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 👨‍💻 Author

Built with ❤️ using Django & Django REST Framework

---

⭐ **If you found this project helpful, please give it a star!**
