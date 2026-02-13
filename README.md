# WorkflowHub 🚀

A modern team workflow management system built with Django. Manage workspaces, projects, tasks, and team collaboration all in one place.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Django](https://img.shields.io/badge/Django-6.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Features

### Workspace Management
- Create and manage multiple workspaces
- Add team members with role-based access
- Track workspace activity and projects

### Project Management
- Create projects within workspaces
- Assign project members with specific roles
- Track project status (Pending, In Progress, Completed, Failed)

### Task Management
- Create and assign tasks to team members
- Track task status (To Do, In Progress, Review, Completed, Failed)
- Set due dates and descriptions

### Comments & Collaboration
- Add comments on tasks
- Nested replies support (threaded comments)
- Real-time collaboration with team

## 🏗️ Project Structure

```
workflow_management_system/
├── accounts/          # Custom user authentication
├── workspaces/        # Workspace management
├── projects/          # Project management
├── tasks/             # Task management
├── comments/          # Task comments & replies
├── templates/         # HTML templates
├── static/            # CSS & JavaScript
│   ├── css/
│   └── js/
└── workflow_hub/      # Main project settings
```

## 🗃️ Database Models

```
Account (Custom User)
    │
    └── Workspace
            │
            ├── WorkspaceMember (role-based)
            │
            └── Project
                    │
                    ├── ProjectMember (role-based)
                    │
                    └── Task
                            │
                            └── TaskComment
                                    │
                                    └── Replies (self-referencing)
```

## 👥 Role System

| Role | Description |
|------|-------------|
| Manager | Full access to workspace/project |
| Leader | Team lead responsibilities |
| Frontend | Frontend developer |
| Backend | Backend developer |
| SEO | SEO specialist |

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/workflow_management_system.git
   cd workflow_management_system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv env
   ```

3. **Activate virtual environment**
   
   Windows:
   ```bash
   env\Scripts\activate
   ```
   
   macOS/Linux:
   ```bash
   source env/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install django
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Open browser**
   ```
   http://127.0.0.1:8000/
   ```

## 📱 URLs

| URL | Description |
|-----|-------------|
| `/` | Home page |
| `/admin/` | Django admin panel |
| `/workspace/` | List all workspaces |
| `/workspace/create/` | Create new workspace |
| `/workspace/<slug>/` | Workspace detail |
| `/projects/` | List all projects |
| `/projects/<workspace>/<project>/` | Project detail |

## 🛠️ Tech Stack

- **Backend:** Django 6.0
- **Database:** SQLite (development)
- **Frontend:** HTML, CSS, JavaScript
- **Styling:** Custom CSS with CSS Variables

## 📸 Screenshots

*Coming soon...*

## 🔜 Upcoming Features

- [ ] User authentication (Login/Logout)
- [ ] Permission system
- [ ] Task status updates
- [ ] Email notifications
- [ ] Dashboard analytics
- [ ] File attachments
- [ ] Activity logs
- [ ] API endpoints (Django REST Framework)

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Your Name**
- First Django project
- MERN Stack Developer transitioning to Django

---

⭐ If you found this project helpful, please give it a star!
