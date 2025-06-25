# Django ERP System

A comprehensive Enterprise Resource Planning (ERP) system built with Django.

## Features

- Employee Management
- Task Management
- Project Management
- Order Management
- Expense Tracking
- Dashboard Analytics
- User Authentication

## Local Development

1. Clone the repository:
```bash
git clone <your-repo-url>
cd ERP-project
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Deployment to Render.com

This project is configured for easy deployment to Render.com.

### Prerequisites

1. GitHub account
2. Render.com account

### Deployment Steps

1. **Push to GitHub:**
   - Create a new repository on GitHub
   - Push this code to your GitHub repository

2. **Deploy on Render:**
   - Go to [Render.com](https://render.com)
   - Click "New +" and select "Web Service"
   - Connect your GitHub repository
   - Use the following settings:
     - **Build Command:** `./build.sh`
     - **Start Command:** `gunicorn config.wsgi:application`
     - **Environment:** `Python 3`

3. **Environment Variables:**
   Set the following environment variables in Render:
   - `SECRET_KEY`: A secure secret key for Django
   - `DEBUG`: `0` (for production)
   - `DJANGO_ALLOWED_HOSTS`: Your Render app URL (e.g., `your-app-name.onrender.com`)
   - `DATABASE_URL`: (Render will provide this if you add a PostgreSQL database)

### Optional: Add PostgreSQL Database

1. In Render dashboard, create a new PostgreSQL database
2. Copy the database URL
3. Add it as `DATABASE_URL` environment variable to your web service

## Project Structure

```
├── config/                 # Django project settings
├── erp_core/              # Main application
├── templates/             # HTML templates
├── static/                # Static files (CSS, JS, images)
├── media/                 # User uploaded files
├── requirements.txt       # Python dependencies
├── build.sh              # Render build script
├── runtime.txt           # Python version for deployment
└── manage.py             # Django management script
```

## Technology Stack

- **Backend:** Django 5.0.2
- **Database:** SQLite (development), PostgreSQL (production)
- **Frontend:** HTML, CSS, Bootstrap 5
- **Forms:** Django Crispy Forms
- **Deployment:** Render.com

## License

This project is open source and available under the [MIT License](LICENSE).
