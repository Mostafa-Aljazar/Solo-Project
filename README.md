# مخيم الأقصى — Al-Aqsa Camp

<p align="center">
  <img src="camp/static/camp/images/logo.png" alt="مخيم الأقصى Logo" width="120" />
</p>

A Django-based humanitarian camp management website for Al-Aqsa Camp, providing shelter, food, healthcare, and education to displaced families in Gaza.

**Live Demo:** [mostafa2003.pythonanywhere.com](https://mostafa2003.pythonanywhere.com)

---

## Features

- **Landing Page** — Hero carousel, mission values, statistics, services, Islamic quote, and CTA sections
- **Blog** — Paginated articles with rich text content and cover images
- **Success Stories** — Real stories from camp beneficiaries with donation links
- **Donations** — Donation form with anonymous option, linked to specific stories
- **Contact Us** — Contact form with email notification to admin (HTML email template)
- **Admin Panel** — Full Django admin for managing all content (slides, articles, donations, messages, statistics, services)
- **Custom Auth** — Email-based login for staff/admin access

---

## Tech Stack

| Layer            | Technology                                    |
| ---------------- | --------------------------------------------- |
| Backend          | Django 6.0.6                                  |
| Database         | MySQL (local) / SQLite (PythonAnywhere)       |
| Rich Text Editor | django-ckeditor 6.7.3                         |
| Image Handling   | Pillow 12.2.0                                 |
| Frontend         | Tailwind CSS (CDN), Cairo font (Google Fonts) |
| Email            | Gmail SMTP via App Password                   |
| Deployment       | PythonAnywhere                                |
| Version Control  | Git / GitHub                                  |

---

## Project Structure

```
SoloProject/
├── SoloProject/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── camp/                 # Main app
│   ├── models.py         # Article, Donation, ContactMessage, HeroSlide, SiteStatistic, Service
│   ├── views.py          # All page views + email logic
│   ├── urls.py
│   ├── admin.py
│   ├── templates/camp/
│   │   ├── home.html
│   │   ├── donate.html
│   │   ├── contact.html
│   │   ├── written_content_list.html
│   │   ├── written_content_detail.html
│   │   └── partials/
│   │       ├── _navbar.html
│   │       └── _footer.html
│   └── static/camp/
│       ├── css/style.css
│       ├── js/camp.js
│       └── images/
├── login/                # Auth app
│   ├── models.py         # Custom User (email-based)
│   ├── views.py          # login_view, logout_view
│   └── templates/login/
├── media/                # Uploaded images (gitignored)
├── staticfiles/          # collectstatic output (gitignored)
├── requirements.txt
└── .env                  # Environment variables (gitignored)
```

---

## Models

| Model            | Description                                                      |
| ---------------- | ---------------------------------------------------------------- |
| `Article`        | Blog articles and success stories (`content_type`: blog / story) |
| `Donation`       | Donations with optional anonymous mode, linked to a story        |
| `ContactMessage` | Messages submitted via the contact form                          |
| `HeroSlide`      | Hero carousel slides with image, title, description, tag         |
| `SiteStatistic`  | Homepage statistics (number + label + icon)                      |
| `Service`        | Humanitarian services displayed on the homepage                  |
| `User`           | Custom user model with email as USERNAME_FIELD                   |

---

## Color Scheme

| Name                   | Hex       |
| ---------------------- | --------- |
| Primary (forest green) | `#345e40` |
| Secondary (sage)       | `#97a483` |
| Dark                   | `#2e2e2e` |

---

## Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/Mostafa-Aljazar/Solo-Project.git
cd Solo-Project/SoloProject

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt
pip install mysqlclient  # required for MySQL — install separately (not in requirements.txt)

# 4. Create .env file
```

`.env` file:

```
USE_SQLITE=False
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=127.0.0.1
DB_PORT=3306
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
CONTACT_EMAIL=your@gmail.com
```

```bash
# 5. Run migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Run server
python manage.py runserver
```

---

## Deployment (PythonAnywhere)

```bash
# On PythonAnywhere console
git clone https://github.com/Mostafa-Aljazar/Solo-Project.git
mkvirtualenv campenv --python=python3.12
cd Solo-Project/SoloProject
pip install -r requirements.txt
# Create .env with USE_SQLITE=True
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

WSGI file (`/var/www/mostafa2003_pythonanywhere_com_wsgi.py`):

```python
import os, sys
sys.path.insert(0, '/home/mostafa2003/Solo-Project')
os.environ['DJANGO_SETTINGS_MODULE'] = 'SoloProject.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Static files mapping in Web tab:

- `/static/` → `/home/mostafa2003/Solo-Project/staticfiles`
- `/media/` → `/home/mostafa2003/Solo-Project/media`

---

## Admin Access

URL: `/admin/login/`

- Manage hero slides, articles, success stories, donations, contact messages, statistics, and services

---

## Developer

**Mostafa Aljazar** — Full Stack Developer

- GitHub: [Mostafa-Aljazar](https://github.com/Mostafa-Aljazar)
