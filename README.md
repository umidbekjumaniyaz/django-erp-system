# ERP System

A modern Enterprise Resource Planning (ERP) system built with Django, featuring project management, task tracking, and expense management.

## Features

- User Authentication and Authorization
- Project Management
- Task Tracking
- Expense Management
- Modern Dashboard
- Responsive Design
- Docker Support
- CI/CD Pipeline

## Tech Stack

- Django 5.0.2
- Bootstrap 5
- SQLite Database
- Docker
- GitHub Actions

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/erp-system.git
cd erp-system
```

2. Create a virtual environment and activate it:
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

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Docker Deployment

1. Build the Docker image:
```bash
docker build -t erp-system .
```

2. Run the container:
```bash
docker run -p 8000:8000 erp-system
```

## Environment Variables

- `DEBUG`: Set to 1 for development, 0 for production
- `SECRET_KEY`: Django secret key
- `DJANGO_ALLOWED_HOSTS`: Allowed hosts (space-separated)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 