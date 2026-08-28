# Modern Django Blog & Polls Application

[![Django](https://img.shields.io/badge/Django-6.0%2B-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![REST Framework](https://img.shields.io/badge/Django_REST_Framework-3.15%2B-red?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

> **Segnotech Internship Project**  
> Developed by **Atul Sain** as part of the Software Engineering Internship at **Segnotech**.

---

## 🌟 Overview

This is a feature-rich, full-stack **Django Web Application** built with modern software architecture best practices. It combines a dynamic content-management Blog system, custom User Authentication & Profiles, interactive Polls, and a powerful **RESTful API** with advanced filtering, phrase search, and pagination.

---

## ✨ Key Features

### 📝 Blog Module (`/blog/`)
- **Full Article Lifecycle**: Create, view, update, and manage blog posts.
- **Categorization & Tagging**: Organize articles with dynamic Categories and multi-select Tags.
- **Nested Comments**: Multi-level hierarchical comment & reply system.
- **Image Uploads**: Automated image and thumbnail generation.
- **Dynamic JavaScript Client**: Asynchronous REST API integration for real-time post loading, search, and filtering without full page reloads.

### 👤 User Authentication & Profiles (`/accounts/`)
- **Custom User Model**: Extended `CustomUser` model supporting profile photo uploads, bio/about, qualification, gender, birth date, and contact numbers.
- **Secure Authentication**: Sign up, log in, log out, session handling, and protected routes (`@login_required`).
- **Profile Management**: Interactive profile view and edit forms with image management.

### 📊 Interactive Polls Module (`/polls/`)
- **Question & Choice System**: Real-time voting interface.
- **Live Results**: Progress bar visualizations for choice vote distribution.

### ⚡ RESTful API (`/api/posts/`)
- **Django REST Framework (DRF)** integration.
- **Filter Backends**: Query posts by `category`, `tag`/`tags` (with slug normalization), `author`, and `slug`.
- **Custom Phrase Search**: Title, content, author, category, and tag phrase matching.
- **Pagination**: Configurable `PageNumberPagination`.
- **Permissions**: `IsAuthenticatedOrReadOnly` for secure endpoint access.

---

## 🛠️ Tech Stack

| Component | Technology Used |
| :--- | :--- |
| **Backend Framework** | Django 6.0+ |
| **API Framework** | Django REST Framework (DRF) |
| **Database** | SQLite3 |
| **Frontend** | HTML5, Modern CSS3, JavaScript (ES6+), Bootstrap 5 |
| **Typography** | Google Fonts (*Plus Jakarta Sans*, *Inter*) |
| **Authentication** | Django Auth System with Custom AbstractUser Model |
| **Filter Engine** | `django-filter` |

---

## 🚀 Quick Start & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Atulsain011/my-first-blog.git
cd my-first-blog
```

### 2. Set Up Virtual Environment
```bash
# On Windows
py -3 -m venv .venv
.venv\Scripts\activate

# On Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations
```bash
python manage.py migrate
```

### 5. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

Open your browser and visit:
- **Blog Application**: `http://127.0.0.1:8000/blog/`
- **Interactive Polls**: `http://127.0.0.1:8000/polls/`
- **REST API Browser**: `http://127.0.0.1:8000/api/posts/`
- **Django Admin Panel**: `http://127.0.0.1:8000/admin/`

---

## 📡 REST API Reference

All API requests are prefixed with `/api/`.

| Endpoint | Method | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `/api/posts/` | `GET` | List all blog posts (paginated) | No |
| `/api/posts/` | `POST` | Create a new blog post | Yes |
| `/api/posts/<slug>/` | `GET` | Retrieve post details by slug | No |
| `/api/posts/<slug>/` | `PUT` / `PATCH` | Update existing post | Yes |
| `/api/posts/<slug>/` | `DELETE` | Delete a post | Yes |

### Query Parameters Example
```http
GET /api/posts/?search=django&category=technology&tag=python&page_size=10
```

---

## 🧪 Automated Testing

Run the full Django test suite (including model tests, API view tests, filters, authentication, and phrase matching):

```bash
python manage.py test
```

---

## 📁 Directory Architecture

```
Django_Project/
├── accounts/               # Custom User & Authentication App
│   ├── forms.py            # SignUp & Profile editing forms
│   ├── models.py           # CustomUser model definition
│   ├── templates/          # Signup, Login, Profile templates
│   ├── urls.py             # Accounts routes
│   └── views.py            # Signup, Profile & Avatar views
├── blog/                   # Main Blog Engine & DRF API App
│   ├── api_urls.py         # REST API routes
│   ├── api_views.py        # DRF ViewSets & FilterSets
│   ├── models.py           # Post, Category, Tag, Comment models
│   ├── pagination.py       # DRF Pagination configuration
│   ├── serializers.py      # DRF Serializers
│   ├── static/             # CSS and static assets
│   ├── templates/          # HTML templates (base, list, detail, edit)
│   ├── tests.py            # Comprehensive test suite
│   ├── urls.py             # HTML blog routes
│   └── views.py            # Django template views
├── polls/                  # Interactive Voting & Polls App
│   ├── admin.py            # Admin configuration
│   ├── models.py           # Question & Choice models
│   ├── templates/          # Index, Detail & Results templates
│   ├── urls.py             # Polls routes
│   └── views.py            # Polls generic views
├── mysite/                 # Core Project Settings & Configuration
│   ├── settings.py         # Django settings configuration
│   ├── urls.py             # Main project URL routing
│   └── wsgi.py / asgi.py   # WSGI/ASGI entrypoints
├── manage.py               # Django CLI utility
├── requirements.txt        # Python package dependencies
└── README.md               # Project documentation
```

---

## 📄 License & Attribution

Developed by **Atul Sain** for **Segnotech Internship**.  
Licensed under the [MIT License](LICENSE).
