# WorkflowHub 🚀

A robust team workflow management system built with **Django 6.0.1**. WorkflowHub helps teams organize work using a clear hierarchy:

```
Workspace → Project → Task → Comment
```

It features secure email-based authentication, role-based access control, email invitations, threaded comments, a full HTML web UI, and a complete REST API with JWT support.

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
15. [Environment Variables](#-environment-variables)
16. [Usage Guide](#-usage-guide)
17. [Production Deployment](#-production-deployment)
18. [Roadmap](#-roadmap)

---

## 🧭 Overview

WorkflowHub is a full-stack Django project management platform. It has two layers:

- **Web UI** — Traditional Django template-based views for browser usage
- **REST API** — Full DRF-based API with JWT authentication for client/mobile apps

### Data Hierarchy

```
Account (User)
 └── Workspace
      ├── WorkspaceMember  (role: manager / leader / frontend / backend / seo)
      ├── WorkspaceInvite  (email invite with UUID token, 7-day expiry)
      └── Project
           ├── ProjectMember  (same role set)
           └── Task
                └── TaskComment  (supports infinite nested replies via self-FK)
```

---

## 📋 Features

- **Custom Auth:** Email-based login using `AbstractBaseUser` + custom `AccountManager`
- **Workspace Management:** Create workspaces, auto-generate unique slugs, manage members with roles
- **Email Invitations:** Invite users to workspaces via email (UUID token, 7-day expiry, accept/reject flow)
- **Project Management:** Projects inside workspaces, status tracking (`pending / in_progress / completed / failed`), role-based creation
- **Task Management:** Assign tasks to project members, set status & due date, 5 status levels
- **Threaded Comments:** Infinite nested replies using self-referential FK on `TaskComment`
- **Soft Delete:** Workspaces and Projects are deactivated (`is_active=False`), not hard-deleted
- **REST API:** Full CRUD API with JWT + Session auth, nested URL structure
- **Role-based Permissions:** 3 custom DRF permission classes (`IsManager`, `IsManagerOrLeader`, `IsProjectMember`)
- **Creator Bypass:** Workspace creator always has manager-level API access even without a `WorkspaceMember` row
- **Query Optimization:** `select_related`, `prefetch_related`, `.annotate()` used throughout to prevent N+1
- **Debug Toolbar:** Integrated `django-debug-toolbar` for development
- **Admin Panel:** Customized admin for all models

---

## 🛠️ Tech Stack

| Category          | Technology                      |
|-------------------|---------------------------------|
| Backend Framework | Django 6.0.1                    |
| API Framework     | Django REST Framework 3.16.1    |
| Authentication    | JWT (simplejwt 5.5.1) + Session |
| Database          | PostgreSQL                      |
| Email             | Resend SMTP                     |
| Frontend          | HTML5, CSS3, Vanilla JavaScript |
| Debug Tools       | Django Debug Toolbar 6.2.0      |
| Config            | python-decouple                 |
| Python Version    | Python 3.x                      |

### Dependencies (`requirements.txt`)

```
asgiref==3.11.0
Django==6.0.1
django-debug-toolbar==6.2.0
djangorestframework==3.16.1
djangorestframework_simplejwt==5.5.1
psycopg2-binary==2.9.11
PyJWT==2.11.0
pyparsing==3.3.2
python-decouple
sqlparse==0.5.5
tzdata==2025.3
```

---

## 📁 Project Structure

```
workflow_management_system/
│
├── manage.py
├── api.http                             # HTTP test file for API requests
├── requirements.txt
├── README.md
├── .env                                 # Environment variables (not committed)
│
├── workflow_hub/                        # Main Django project config
│   ├── settings.py                      # All settings (DB, email, DRF, etc.)
│   ├── urls.py                          # Root URL config
│   ├── views.py                         # Home view
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/                            # Custom user authentication
│   ├── models.py                        # Account, AccountManager
│   ├── views.py                         # login, register, logout, profile
│   ├── urls.py
│   └── admin.py                         # Custom AccountAdmin (UserAdmin)
│
├── workspaces/                          # Workspace management
│   ├── models.py                        # Workspace, WorkspaceMember
│   ├── views.py                         # CRUD + member management + settings
│   ├── urls.py
│   └── admin.py
│
├── invitations/                         # Email-based workspace invitations
│   ├── models.py                        # WorkspaceInvite (UUID token, expiry)
│   ├── views.py                         # send_invite, get_invites (accept/reject)
│   ├── forms.py                         # WorkspaceInviteForm
│   ├── urls.py
│   └── admin.py
│
├── projects/                            # Project management
│   ├── models.py                        # Project, ProjectMember
│   ├── views.py                         # CRUD + member management + settings
│   ├── urls.py
│   └── admin.py
│
├── tasks/                               # Task management
│   ├── models.py                        # Task
│   ├── views.py                         # get_all_tasks, add_task
│   ├── urls.py
│   └── admin.py
│
├── comments/                            # Threaded comments on tasks
│   ├── models.py                        # TaskComment (self-FK for nested replies)
│   ├── views.py                         # view_all_comments (GET + POST)
│   ├── urls.py
│   └── admin.py
│
├── api/                                 # REST API layer (DRF)
│   ├── urls.py                          # All API routes
│   ├── permissions.py                   # IsManager, IsManagerOrLeader, IsProjectMember
│   ├── serializers/
│   │   ├── __init__.py
│   │   ├── common_serializers.py        # UserSerializer
│   │   ├── workspace.py                 # WorkspaceSerializer, WorkspaceMemberSerializer
│   │   ├── workspace_members.py         # WorkSpaceMemberSerializer (used in members view)
│   │   ├── workspace_projects.py        # WorkspaceProjectSerializer, WorkspaceProjectDetailSerializer
│   │   ├── project_member_serializer.py # ProjectMemberSerializer
│   │   ├── task_serializers.py          # ProjectTaskSerializer, CreateTaskSerializer
│   │   ├── comment_serializer.py        # CommentSerializer + CommentPagination (5/page)
│   │   └── comment_reply_serializer.py  # CommentDetailSerializer (recursive replies)
│   └── views/
│       ├── __init__.py
│       ├── workspace.py                 # ListCreate + RetrieveUpdateDestroy workspace
│       ├── workspace_members.py         # ListCreate workspace members
│       ├── workspace_projects.py        # Projects, Tasks, ProjectMembers list/create views
│       ├── project_task_details.py      # Retrieve/Update/Delete single task
│       └── task_comments.py             # Paginated threaded comments
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
│   │   └── tast_comments_details.html
│   ├── invitations/
│   │   ├── send_invite.html
│   │   └── all_invites.html
│   └── includes/
│
├── static/
│   ├── css/style.css
│   └── js/index.js
│
└── env/                                 # Virtual environment (not committed)
```
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
View Function (inline role check → PermissionDenied if failed)
    │
    ▼
ORM Queries (Models — select_related / prefetch_related)
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
IsAuthenticated  →  IsManager / IsManagerOrLeader / IsProjectMember
    │
    ▼
GenericAPIView → get_serializer_class() → Serializer validation
    │
    ▼
ORM Queries (annotated + optimized) → JSON Response
```

---

## 🗃️ Database Models

### Entity Relationship

```
Account
 ├── Workspace  (created_workspaces)
 │     ├── WorkspaceMember  ←── Account  (user, role, is_active)
 │     ├── WorkspaceInvite  (email, token, status, expires_at)
 │     └── Project  (created_by → Account)
 │           ├── ProjectMember  ←── Account  (member, role, is_active)
 │           └── Task
 │                 ├── assigned_to → ProjectMember
 │                 ├── created_by  → Account
 │                 └── TaskComment
 │                       └── parent_comment → TaskComment  (self-referential)
```

---

### 1. `Account` — `accounts/models.py`

| Field           | Type            | Notes                                  |
|-----------------|-----------------|----------------------------------------|
| `first_name`    | CharField(50)   |                                        |
| `last_name`     | CharField(50)   |                                        |
| `username`      | CharField(100)  | unique                                 |
| `email`         | EmailField(100) | unique · `USERNAME_FIELD`              |
| `phone_number`  | CharField(50)   | optional (blank=True)                  |
| `date_joined`   | DateTimeField   | auto_now_add                           |
| `last_login`    | DateTimeField   | auto_now                               |
| `is_admin`      | BooleanField    | default False                          |
| `is_staff`      | BooleanField    | default False                          |
| `is_active`     | BooleanField    | default True                           |
| `is_superadmin` | BooleanField    | default False                          |

`USERNAME_FIELD = 'email'` · `REQUIRED_FIELDS = ['username', 'first_name', 'last_name']`

---

### 2. `Workspace` — `workspaces/models.py`

| Field        | Type           | Notes                               |
|--------------|----------------|-------------------------------------|
| `name`       | CharField(100) |                                     |
| `slug`       | SlugField(100) | unique · auto-generated on `save()` |
| `creator`    | FK → Account   | CASCADE · `created_workspaces`      |
| `is_active`  | BooleanField   | default True · soft-delete flag     |
| `created_at` | DateTimeField  | auto_now_add                        |
| `updated_at` | DateTimeField  | auto_now                            |

> **Auto-slug:** Generated from `name` on first save. Collisions resolved with `-1`, `-2`, etc. Update slug regeneration uses `.exclude(pk=instance.pk)` to avoid self-collision.

---

### 3. `WorkspaceMember` — `workspaces/models.py`

| Field       | Type           | Notes                                      |
|-------------|----------------|--------------------------------------------|
| `workspace` | FK → Workspace | CASCADE · `members`                        |
| `user`      | FK → Account   | CASCADE · `workspace_memberships`          |
| `role`      | CharField(20)  | choices — see [Role System](#-role-system) |
| `joined_at` | DateTimeField  | auto_now_add                               |
| `is_active` | BooleanField   | default True                               |

`unique_together = ('workspace', 'user')`

---

### 4. `WorkspaceInvite` — `invitations/models.py`

| Field        | Type           | Notes                                           |
|--------------|----------------|-------------------------------------------------|
| `workspace`  | FK → Workspace | CASCADE · `invites`                             |
| `email`      | EmailField     | Recipient email                                 |
| `invited_by` | FK → Account   | CASCADE · `sent_invites`                        |
| `role`       | CharField(20)  | Role to assign on acceptance                    |
| `token`      | UUIDField      | unique · auto-generated · not editable          |
| `status`     | CharField(20)  | `pending` / `accepted` / `rejected` / `expired` |
| `created_at` | DateTimeField  | auto_now_add                                    |
| `expires_at` | DateTimeField  | Auto-set to 7 days from creation                |

`unique_together = ('workspace', 'email')` · `is_expired()` helper method included.

> **Flow:** Manager sends invite → Email sent via Resend SMTP → Recipient visits `/invitations/all_invites/` → Accept creates `WorkspaceMember` row → Reject marks status as `rejected`.

---

### 5. `Project` — `projects/models.py`

| Field        | Type           | Notes                                              |
|--------------|----------------|----------------------------------------------------|
| `workspace`  | FK → Workspace | CASCADE · `projects`                               |
| `name`       | CharField(150) |                                                    |
| `slug`       | SlugField(150) | auto-generated on `save()`                         |
| `status`     | CharField(20)  | `pending` / `in_progress` / `completed` / `failed` |
| `created_by` | FK → Account   | SET_NULL · `created_projects`                      |
| `is_active`  | BooleanField   | default True · soft-delete flag                    |
| `created_at` | DateTimeField  | auto_now_add                                       |
| `updated_at` | DateTimeField  | auto_now                                           |

`unique_together = ('workspace', 'slug')` · `ordering = ['-created_at']`

---

### 6. `ProjectMember` — `projects/models.py`

| Field        | Type          | Notes                                      |
|--------------|---------------|--------------------------------------------|
| `member`     | FK → Account  | CASCADE · `project_memberships`            |
| `project`    | FK → Project  | CASCADE · `members`                        |
| `role`       | CharField(50) | choices — see [Role System](#-role-system) |
| `is_active`  | BooleanField  | default True                               |
| `joined_at`  | DateTimeField | auto_now_add                               |
| `updated_at` | DateTimeField | auto_now                                   |

`unique_together = ('project', 'member')`

---

### 7. `Task` — `tasks/models.py`

| Field         | Type               | Notes                                                |
|---------------|--------------------|------------------------------------------------------|
| `project`     | FK → Project       | CASCADE · `tasks`                                    |
| `title`       | CharField(200)     |                                                      |
| `description` | TextField          | blank=True                                           |
| `assigned_to` | FK → ProjectMember | SET_NULL · null=True · blank=True · `tasks`          |
| `created_by`  | FK → Account       | SET_NULL · null=True · `created_tasks`               |
| `status`      | CharField(20)      | `todo` / `in_progress` / `review` / `completed` / `failed` |
| `due_date`    | DateField          | null=True · blank=True                               |
| `created_at`  | DateTimeField      | auto_now_add                                         |
| `updated_at`  | DateTimeField      | auto_now                                             |

---

### 8. `TaskComment` — `comments/models.py`

| Field            | Type          | Notes                                        |
|------------------|---------------|----------------------------------------------|
| `task`           | FK → Task     | CASCADE · `comments`                         |
| `author`         | FK → Account  | SET_NULL · null=True · `task_comments`       |
| `parent_comment` | FK → self     | CASCADE · null=True · blank=True · `replies` |
| `content`        | TextField     |                                              |
| `created_at`     | DateTimeField | auto_now_add                                 |
| `updated_at`     | DateTimeField | auto_now                                     |

> Top-level comments: `parent_comment=None`. Replies: `parent_comment=<comment>`. Recursively serialized via `CommentDetailSerializer.get_replies()`.

---

## 👥 Role System

Both `WorkspaceMember` and `ProjectMember` share the same role options:

| Role       | Label               | Create Project | Add WS Members (API) | Add Project Members (API) |
|------------|---------------------|:--------------:|:--------------------:|:-------------------------:|
| `manager`  | Manager             | ✅             | ✅                   | ✅                        |
| `leader`   | Leader              | ✅             | ❌                   | ✅                        |
| `frontend` | Frontend Developer  | ❌             | ❌                   | ❌                        |
| `backend`  | Backend Developer   | ❌             | ❌                   | ❌                        |
| `seo`      | SEO                 | ❌             | ❌                   | ❌                        |

**Auto-assignments:**
- Workspace **creator** → automatically added to `WorkspaceMember` as `manager` on creation
- Project **creator** → automatically added to `ProjectMember` as `manager` via `get_or_create`
- Workspace **creator** also bypasses `WorkspaceMember` lookup in API permissions (creator always has manager-level access)

---

## 🔗 URL Routes

### Web Application

| URL                                                  | View                       | URL Name                   |
|------------------------------------------------------|----------------------------|----------------------------|
| `/`                                                  | `home`                     | `home`                     |
| `/accounts/login/`                                   | `login_view`               | `login`                    |
| `/accounts/register/`                                | `register_view`            | `register`                 |
| `/accounts/logout/`                                  | `logout_view`              | `logout`                   |
| `/accounts/profile/`                                 | `profile_view`             | `profile`                  |
| `/workspace/`                                        | `workspaces`               | `workspaces`               |
| `/workspace/create/`                                 | `create_workspace`         | `create_workspace`         |
| `/workspace/<slug>/`                                 | `workspace_detail`         | `workspace_detail`         |
| `/workspace/<slug>/add_member/`                      | `add_member_in_workspace`  | `add_member`               |
| `/workspace/<slug>/create_project/`                  | `create_workspace_project` | `create_workspace_project` |
| `/workspace/<slug>/settings/`                        | `workspace_settings`       | `workspace_settings`       |
| `/workspace/<slug>/invite/`                          | `send_invite`              | `send_invite`              |
| `/invitations/all_invites/`                          | `get_invites`              | `all_invites`              |
| `/projects/`                                         | `projects`                 | `projects`                 |
| `/projects/<ws_slug>/<proj_slug>/`                   | `project_detail`           | `project_detail`           |
| `/projects/<ws_slug>/<proj_slug>/add_new_member`     | `add_member`               | `add_member`               |
| `/projects/<ws_slug>/<proj_slug>/settings/`          | `project_settings`         | `project_settings`         |
| `/projects/<ws_slug>/<proj_slug>/task/add_task`      | `add_task`                 | `add_project_task`         |
| `/tasks/get_all_tasks/`                              | `get_all_tasks`            | `get_all_tasks`            |
| `/projects/<ws_slug>/<proj_slug>/comment/<id>/`      | `view_all_comments`        | `view_comment_details`     |

### REST API

| Method       | Endpoint                                                                | Description                          | Permission                       |
|--------------|-------------------------------------------------------------------------|--------------------------------------|----------------------------------|
| `POST`       | `/api/token/`                                                           | Obtain JWT access + refresh tokens   | Public                           |
| `POST`       | `/api/token/refresh/`                                                   | Refresh access token                 | Public                           |
| `GET`        | `/api/workspaces/`                                                      | List user's workspaces (annotated)   | IsAuthenticated                  |
| `POST`       | `/api/workspaces/`                                                      | Create workspace                     | IsAuthenticated                  |
| `GET`        | `/api/workspaces/<slug>/`                                               | Workspace detail                     | IsAuthenticated                  |
| `PUT/PATCH`  | `/api/workspaces/<slug>/`                                               | Update workspace name                | IsAuthenticated + **IsManager**  |
| `DELETE`     | `/api/workspaces/<slug>/`                                               | Delete workspace                     | IsAuthenticated + **IsManager**  |
| `GET`        | `/api/workspaces/<slug>/members/`                                       | List workspace members               | IsAuthenticated                  |
| `POST`       | `/api/workspaces/<slug>/members/`                                       | Add member to workspace              | IsAuthenticated + **IsManager**  |
| `GET`        | `/api/workspaces/<slug>/projects/`                                      | List projects in workspace           | IsAuthenticated                  |
| `POST`       | `/api/workspaces/<slug>/projects/`                                      | Create project                       | IsAuthenticated                  |
| `GET`        | `/api/workspaces/<slug>/projects/<proj_slug>/`                          | Project detail (with members, stats) | IsAuthenticated + **IsManagerOrLeader** (project member for GET) |
| `PUT/PATCH`  | `/api/workspaces/<slug>/projects/<proj_slug>/`                          | Update project                       | IsAuthenticated + **IsManagerOrLeader** |
| `DELETE`     | `/api/workspaces/<slug>/projects/<proj_slug>/`                          | Delete project                       | IsAuthenticated + **IsManagerOrLeader** |
| `GET`        | `/api/workspaces/<slug>/projects/<proj_slug>/members/`                  | List project members                 | IsAuthenticated + **IsManagerOrLeader** |
| `POST`       | `/api/workspaces/<slug>/projects/<proj_slug>/members/`                  | Add project member                   | IsAuthenticated + **IsManagerOrLeader** |
| `GET`        | `/api/workspaces/<slug>/projects/<proj_slug>/tasks/`                    | List tasks                           | IsAuthenticated + **IsProjectMember** |
| `POST`       | `/api/workspaces/<slug>/projects/<proj_slug>/tasks/`                    | Create task                          | IsAuthenticated + **IsProjectMember** |
| `GET`        | `/api/workspaces/<slug>/projects/<proj_slug>/tasks/<id>/`               | Task detail                          | IsAuthenticated + **IsProjectMember** |
| `PUT/PATCH`  | `/api/workspaces/<slug>/projects/<proj_slug>/tasks/<id>/`               | Update task                          | IsAuthenticated + **IsProjectMember** |
| `DELETE`     | `/api/workspaces/<slug>/projects/<proj_slug>/tasks/<id>/`               | Delete task                          | IsAuthenticated + **IsProjectMember** |
| `GET`        | `/api/workspaces/<slug>/projects/<proj_slug>/tasks/<id>/comments/`      | Paginated threaded comments (5/page) | IsAuthenticated + **IsProjectMember** |
| `POST`       | `/api/workspaces/<slug>/projects/<proj_slug>/tasks/<id>/comments/`      | Add comment or reply                 | IsAuthenticated + **IsProjectMember** |

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

### `invitations/views.py`

| View          | Logic                                                                                    |
|---------------|-----------------------------------------------------------------------------------------|
| `send_invite` | Manager-only POST: validates email not already a member, creates `WorkspaceInvite` (UUID token, 7-day expiry), sends invite email via `send_mail()` using Resend SMTP |
| `get_invites` | GET: lists all pending invites for logged-in user by email. Accept creates `WorkspaceMember` and marks invite accepted; Reject marks invite rejected |

---

## 🌐 REST API Views

| View Class                         | Base Class                     | Purpose                                     |
|------------------------------------|--------------------------------|---------------------------------------------|
| `ListCreateWorkspaceView`          | `ListCreateAPIView`            | List (annotated) + create workspaces        |
| `WorkSpaceDetailView`              | `RetrieveUpdateDestroyAPIView` | Workspace CRUD by slug                      |
| `ListCreateWorkspaceMembersApiView`| `ListCreateAPIView`            | Members list + add (`IsManager` on POST)    |
| `WorkspaceProjectApiView`          | `ListCreateAPIView`            | Project list + create                       |
| `WorkspaceProjectDetailsApiView`   | `RetrieveUpdateDestroyAPIView` | Project detail/update/delete (`IsManagerOrLeader`) |
| `ProjectMembersApiView`            | `ListCreateAPIView`            | Project members list + add (`IsManagerOrLeader`) |
| `ProjectTasksApiView`              | `ListCreateAPIView`            | Task list + create (`IsProjectMember`)      |
| `RetrieveTaskApiView`              | `RetrieveUpdateDestroyAPIView` | Task detail/update/delete (`IsProjectMember`) |
| `TaskCommentsAPIView`              | `ListCreateAPIView`            | Paginated threaded comments (`IsProjectMember`) |

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

### REST API — 3 Custom Permission Classes

```python
# api/permissions.py

class IsManager(permissions.BasePermission):
    """Allow write access only to workspace managers or the workspace creator."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        workspace_slug = view.kwargs.get("workspace_slug")
        if not workspace_slug:
            return False
        # Creator always has manager-level access
        if Workspace.objects.filter(creator=request.user, slug=workspace_slug).exists():
            return True
        return WorkspaceMember.objects.filter(
            workspace__slug=workspace_slug,
            user=request.user,
            role='manager',
            is_active=True
        ).exists()


class IsManagerOrLeader(permissions.BasePermission):
    """Allow write access to workspace managers, leaders, or the workspace creator."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        workspace_slug = view.kwargs.get("workspace_slug")
        if not workspace_slug:
            return False
        # Creator always has manager-level access
        if Workspace.objects.filter(creator=request.user, slug=workspace_slug).exists():
            return True
        return WorkspaceMember.objects.filter(
            workspace__slug=workspace_slug,
            user=request.user,
            role__in=['manager', 'leader'],
            is_active=True
        ).exists()


class IsProjectMember(permissions.BasePermission):
    """Allow access only to members of the specific project."""
    def has_permission(self, request, view):
        workspace_slug = view.kwargs.get("workspace_slug")
        project_slug = view.kwargs.get("project_slug")
        return ProjectMember.objects.filter(
            project__slug=project_slug,
            project__workspace__slug=workspace_slug,
            member__user=request.user,
            is_active=True
        ).exists()
```

**Permission Summary:**

| Class | Applied To | Condition |
|---|---|---|
| `IsManager` | Workspace member add, workspace update/delete | Must be workspace `manager` role OR workspace creator |
| `IsManagerOrLeader` | Project CRUD, project member management | Must be workspace `manager` or `leader` OR workspace creator |
| `IsProjectMember` | Task CRUD, task comments | Must be an active member of the specific project |

> **Creator Bypass**: The workspace creator is granted manager-level access in both `IsManager` and `IsManagerOrLeader` even if they have no `WorkspaceMember` record.

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

**6. Create a `.env` file in the project root**
```env
RESEND_API_KEY=re_your_resend_api_key_here
```
> Get a free API key at [resend.com](https://resend.com). Required for workspace invitation emails.

**7. Run migrations**
```bash
python manage.py migrate
```

**8. Create superuser**
```bash
python manage.py createsuperuser
```

**9. Run development server**
```bash
python manage.py runserver
```

**10. Access the app**

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

### Email Settings (Resend SMTP)

| Setting            | Value                        | Purpose                          |
|--------------------|------------------------------|----------------------------------|
| `EMAIL_BACKEND`    | `django.core.mail.backends.smtp.EmailBackend` | SMTP email backend  |
| `EMAIL_HOST`       | `smtp.resend.com`            | Resend SMTP server               |
| `EMAIL_PORT`       | `587`                        | TLS port                         |
| `EMAIL_USE_TLS`    | `True`                       | Enable TLS encryption            |
| `EMAIL_HOST_USER`  | `resend`                     | Fixed username for Resend        |
| `EMAIL_HOST_PASSWORD` | `config('RESEND_API_KEY')` | Loaded from `.env` via python-decouple |
| `DEFAULT_FROM_EMAIL` | `onboarding@resend.dev`    | Sender address for invite emails |

---

## 🔑 Environment Variables

The project uses [`python-decouple`](https://pypi.org/project/python-decouple/) to load sensitive values from a `.env` file.

### `.env` file (create in project root, never commit)

```env
# Resend API Key — required for workspace invitation emails
RESEND_API_KEY=re_your_resend_api_key_here
```

### Getting a Resend API Key

1. Sign up at [resend.com](https://resend.com/signup)
2. Go to **API Keys** → **Create API Key**
3. Copy the key and paste it in your `.env` file
4. Verify a sending domain in Resend dashboard and update `DEFAULT_FROM_EMAIL` in `settings.py`

> **Note**: Without a valid `RESEND_API_KEY`, the app runs normally but invitation emails will fail to send. For development, you can use Django's console email backend instead:
> ```python
> EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
> ```

---

## 📖 Usage Guide

### Web App Workflow

1. **Register** at `/accounts/register/`
2. **Login** at `/accounts/login/` using email & password
3. **Create Workspace** — you are auto-assigned as `manager`
4. **Invite Members by Email** — go to `/workspace/<slug>/invite/` (manager only), enter email and role; the invitee receives an email with an accept/reject link
5. **Accept Invite** — invitee visits `/invitations/all_invites/` while logged in and accepts; they are added as a `WorkspaceMember` with the assigned role
6. **Add Members Directly** — alternatively, use `/workspace/<slug>/add_member/` to add existing registered users without email
7. **Create Project** — only manager or leader can create
8. **Add Project Members** — from existing workspace members
9. **Create Tasks** — assign to project members, set status & due date
10. **Track Tasks** — view all assigned/created tasks at `/tasks/get_all_tasks/`
11. **Comment** — add threaded comments/replies on tasks
12. **Settings** — soft-delete projects or workspaces (manager only)

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

**Reply to a comment** (set `parent_comment` to the comment ID)
```bash
curl -X POST http://127.0.0.1:8000/api/workspaces/my-ws/projects/my-proj/tasks/1/comments/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "Thanks for the review!", "parent_comment": 5}'
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
- [x] Email-based workspace invitations (Resend SMTP + `WorkspaceInvite` model)
- [x] Fixed: Double `super().perform_create()` call in `ListCreateWorkspaceView`
- [x] Fixed: Infinite loop during slug update (`perform_update` now excludes current instance)
- [x] Fixed: `Workspace/Project.objects.get()` replaced with `get_object_or_404()` in API views
- [x] Fixed: `IsManager` null check for missing `workspace_slug` kwarg
- [x] Fixed: `get_comments` serializer returned only 1 comment (removed `[:1]` slice)
- [x] Fixed: Workspace creator bypasses `WorkspaceMember` lookup in `IsManager` and `IsManagerOrLeader`
- [x] Added `ProjectMembersApiView` endpoint for listing and adding project members
- [x] Fixed: `python-decouple` added to `requirements.txt`
- [ ] Fix `send_invite` in `invitations/views.py` — missing creator bypass in permission check
- [ ] Fix `comments/views.py` — replace list index lookup with `get_object_or_404` to avoid `IndexError`
- [ ] Move all DB credentials and `SECRET_KEY` to `.env` file
- [ ] Production setup (`.env`, gunicorn, whitenoise, `DEBUG=False`)
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
