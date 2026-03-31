# WorkflowHub 🚀

A **production-grade, real-time team workflow management system** built with:

* **Django 6**
* **Django REST Framework**
* **Django Channels (WebSockets)**
* **Redis**

WorkflowHub enables teams to collaborate efficiently using a structured hierarchy:

```
Workspace → Project → Task → Comment → Reaction
```

---

# 🔥 Key Highlights

* ⚡ Real-time updates (WebSockets + Redis)
* 🧠 Event-driven architecture (Django Signals)
* 🔐 Role-based access control (RBAC)
* 💬 Threaded comments (infinite nesting)
* 👍 Like / Dislike reactions (toggle system)
* 🚀 Optimized ORM queries (no N+1 problem)
* 🔑 JWT + Session Authentication

---

# 📑 Table of Contents

1. Overview
2. Features
3. Tech Stack
4. Project Structure
5. Architecture
6. Real-Time System
7. Database Models
8. Role System
9. API & Routes
10. Permissions
11. Installation
12. Configuration
13. Usage
14. Production Deployment
15. Roadmap

---

# 🧭 Overview

WorkflowHub is a **full-stack + real-time collaboration platform** with:

### Two Layers

* **Web UI (Django Templates)**
* **REST API (DRF + JWT)**

---

## 🧱 Data Hierarchy

```
Account
 └── Workspace
      ├── WorkspaceMember
      ├── WorkspaceInvite
      └── Project
           ├── ProjectMember
           └── Task
                ├── TaskComment
                └── CommentReaction
```

---

# 📋 Features

## 🧩 Core Features

* Custom email-based authentication
* Workspace & project management
* Role-based permissions
* Task assignment with status & due dates
* Threaded comments (nested replies)
* Soft delete system

---

## ⚡ Real-Time Features

* Live task updates
* Live comments & replies
* Live reactions
* Multi-user sync (instant UI)

---

## 👍 Reaction System

* Like / Dislike
* Toggle logic:

  * like → dislike
  * dislike → remove
* One reaction per user

---

# 🛠️ Tech Stack

| Category  | Tech                        |
| --------- | --------------------------- |
| Backend   | Django 6                    |
| API       | DRF                         |
| Auth      | JWT + Session               |
| DB        | PostgreSQL                  |
| Real-time | Channels + Redis            |
| Frontend  | HTML / JS / (Next.js ready) |

---

# 📁 Project Structure

```
workflow_management_system/
│
├── workflow_hub/        # Django config (ASGI ready)
├── accounts/            # Custom auth
├── workspaces/          # Workspaces
├── projects/            # Projects
├── tasks/               # Tasks
├── comments/            # Comments + reactions
├── invitations/         # Email invites
├── api/                 # DRF layer
│   ├── serializers/
│   ├── views/
│   └── permissions.py
│
├── templates/
├── static/
```

---

# 🏛️ Architecture

## Web Flow

```
Request → URL → View → ORM → Template → Response
```

## API Flow

```
Request → Auth → Permission → Serializer → ORM → JSON
```

---

# ⚡ Real-Time System

## Architecture

```
Frontend
   ↓
WebSocket
   ↓
Django Channels
   ↓
Redis
   ↓
Signals
   ↓
Broadcast (project_<slug>)
```

---

## Events

* task_created
* task_updated
* comment_created
* reaction_updated

---

## Flow

```
User Action → Save → Signal → Channel → WebSocket → UI Update
```

---

# 🗃️ Database Models

## Key Models

### Account

Custom user model (email login)

### Workspace

* slug auto-generated
* soft delete

### Project

* belongs to workspace
* role controlled

### Task

* assigned_to
* due_date
* 5 statuses

### TaskComment

* self-relation (nested replies)

### CommentReaction

* like/dislike
* unique(user, comment)

---

# 👥 Role System

| Role                 | Access          |
| -------------------- | --------------- |
| manager              | full access     |
| leader               | project control |
| frontend/backend/seo | limited         |

👉 Workspace creator = always manager

---

# 🌐 API Overview

```
/api/workspaces/
/api/projects/
/api/tasks/
/api/comments/
/api/reactions/
```

---

# 🔐 Permissions

* IsManager
* IsManagerOrLeader
* IsProjectMember

👉 Creator bypass included

---

# 🚀 Installation

```bash
git clone <repo>
cd workflow_management_system

python -m venv env
source env/bin/activate

pip install -r requirements.txt
```

---

## DB Setup

```sql
CREATE DATABASE workflow_db;
```

---

## Run

```bash
python manage.py migrate
python manage.py runserver
```

---

## Redis (IMPORTANT)

```bash
redis-server
```

---

# ⚙️ Environment Variables

```
SECRET_KEY=your_secret
DEBUG=True
DB_NAME=workflow_db
DB_USER=postgres
DB_PASSWORD=yourpassword
RESEND_API_KEY=your_api_key
```

---

# 📖 Usage Flow

1. Register
2. Create workspace
3. Invite members
4. Create project
5. Assign tasks
6. Comment + react
7. Real-time updates auto sync

---

# 🚀 Production Notes

Before deploy:

* DEBUG = False
* Use .env
* Use gunicorn
* Use whitenoise
* Add ALLOWED_HOSTS

---

# 📈 Roadmap

* Notifications system
* File uploads
* Activity logs
* Analytics dashboard
* Kanban board

---

# 💬 Final Note

This project demonstrates:

* Real-time backend engineering
* Scalable architecture
* Clean Django + DRF design

---

# 👨‍💻 Author

Built with ❤️ using Django, DRF & WebSockets

---

⭐ Star this repo if useful!
