# Job Board Platform

The Job Board Platform Backend is an enterprise-grade RESTful API designed to power modern job board platforms. It is a robust, scalable, and production-ready backend system for a comprehensive job board platform built with Django, PostgreSQL, and JWT authentication.
It provides comprehensive features for managing job postings, user applications, optimized job search capabilities, comprehensive API documentation, and role-based access control with a focus on performance, security, and scalability.

## 🚀 Features

### Core Functionality

- **Job Posting Management**: Complete CRUD operations for job postings
- **Category Management**: Organize jobs by industry, location, and type
- **Application System**: Users can apply for jobs and track applications
- **Role-Based Access Control**: Separate permissions for admins and users
- **Optimized Search**: Fast, indexed queries with multiple filter options
- **API Documentation**: Interactive Swagger/OpenAPI documentation

### Technical Highlights

- **JWT Authentication**: Secure token-based authentication
- **Database Optimization**: Indexed queries for efficient data retrieval
- **RESTful API Design**: Clean, consistent API endpoints
- **Comprehensive Testing**: Unit and integration tests
- **Docker Support**: Containerized deployment ready

## 🛠️ Technologies Used

| Technology            | Purpose                                    |
| --------------------- | ------------------------------------------ |
| Django 5.0            | High-level Python web framework            |
| Django REST Framework | RESTful API development                    |
| PostgreSQL 15         | Primary database                           |
| JWT (Simple JWT)      | Token-based authentication                 |
| drf-spectacular       | OpenAPI 3.0 schema generation & Swagger UI |
| Docker                | Containerization                           |
| Gunicorn              | WSGI HTTP Server                           |
| Nginx                 | Reverse proxy (production)                 |

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Docker & Docker Compose (optional)
- pip & virtualenv

## 🔧 Installation & Setup

### Option 1: Local Development

1. **Clone the repository**

```bash
git clone https://github.com/LennyBeto/job-board-platform.git
cd job-board-platform
```

2. **Create and activate virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Set up PostgreSQL database**

```bash
# Create database
createdb prodev_jobboard

# Or using psql
psql -U postgres
CREATE DATABASE prodev_jobboard;
```

6. **Run migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

7. **Create superuser**

```bash
python manage.py createsuperuser
```

8. **Run development server**

```bash
python manage.py runserver
```

### Option 2: Docker

1. **Clone and configure**

```bash
git clone https://github.com/LennyBeto/job-board-platform.git
cd job-board-platform
cp .env.example .env
```

2. **Build and run containers**

```bash
docker-compose up --build
```

3. **Create superuser**

```bash
docker-compose exec web python manage.py createsuperuser
```

## 🔑 Environment Variables

Create a `.env` file with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=prodev_jobboard
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=60  # minutes
JWT_REFRESH_TOKEN_LIFETIME=1440  # minutes (24 hours)

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

## 📚 API Documentation

Access the interactive API documentation at:

- **Swagger UI**: `http://localhost:8000/api/docs/`
- **ReDoc**: `http://localhost:8000/api/redoc/`
- **OpenAPI Schema**: `http://localhost:8000/api/schema/`

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication.

### Obtaining Tokens

**POST** `/api/auth/token/`

```json
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

**Response:**

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Using Tokens

Include the access token in the Authorization header:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

## 🎯 API Endpoints

### Authentication

- `POST /api/auth/register/` - Register new user
- `POST /api/auth/token/` - Obtain JWT token pair
- `POST /api/auth/token/refresh/` - Refresh access token
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/` - Update user profile

### Jobs

- `GET /api/jobs/` - List all jobs (with filtering)
- `POST /api/jobs/` - Create job (admin only)
- `GET /api/jobs/{id}/` - Retrieve job details
- `PUT /api/jobs/{id}/` - Update job (admin only)
- `DELETE /api/jobs/{id}/` - Delete job (admin only)

### Categories

- `GET /api/categories/` - List all categories
- `POST /api/categories/` - Create category (admin only)
- `GET /api/categories/{id}/` - Retrieve category
- `PUT /api/categories/{id}/` - Update category (admin only)
- `DELETE /api/categories/{id}/` - Delete category (admin only)

### Applications

- `GET /api/applications/` - List user's applications
- `POST /api/applications/` - Apply for a job
- `GET /api/applications/{id}/` - Retrieve application
- `PUT /api/applications/{id}/` - Update application
- `DELETE /api/applications/{id}/` - Withdraw application

## 🔍 Query Parameters

### Job Filtering

```
GET /api/jobs/?category=1&location=Nairobi&job_type=full-time&search=developer
```

Available filters:

- `category` - Filter by category ID
- `location` - Filter by location (case-insensitive)
- `job_type` - Filter by job type (full-time, part-time, contract, internship)
- `salary_min` - Minimum salary
- `salary_max` - Maximum salary
- `search` - Search in title and description
- `ordering` - Sort results (e.g., `-created_at`, `salary`)

## 👥 User Roles

### Admin

- Create, update, and delete jobs
- Manage categories
- View all applications
- Access admin panel

### User (Regular)

- View all jobs
- Apply for jobs
- Manage own applications
- Update own profile

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python manage.py test

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html

# Run specific app tests
python manage.py test apps.jobs
python manage.py test apps.authentication

# Using pytest
pytest
pytest --cov=apps
```

## 🚀 Deployment

### Heroku Deployment

1. **Install Heroku CLI**
2. **Create Heroku app**

```bash
heroku create prodev-job-board
```

3. **Add PostgreSQL addon**

```bash
heroku addons:create heroku-postgresql:mini
```

4. **Set environment variables**

```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
```

5. **Deploy**

```bash
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Railway/Render Deployment

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed deployment instructions.

## 📊 Database Schema

The application uses a normalized PostgreSQL schema with the following main models:

- **User**: Custom user model with role management
- **Category**: Job categories (industry-based)
- **Job**: Job postings with details
- **Application**: User job applications

See [DATABASE_SCHEMA.md](docs/DATABASE_SCHEMA.md) for detailed schema documentation.

## 🔧 Performance Optimizations

- **Database Indexing**: Indexes on frequently queried fields
- **Query Optimization**: Select_related and prefetch_related for reducing queries
- **Pagination**: Default pagination for list endpoints
- **Caching**: Redis caching for frequently accessed data (optional)

## 📝 Git Workflow

Follow conventional commits:

```bash
feat: add job application feature
fix: resolve authentication bug
perf: optimize job search queries
docs: update API documentation
test: add job model tests
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/amazing-feature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push to branch (`git push origin feat/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Lenny Beto - [GitHub](https://github.com/LennyBeto)

## 🙏 Acknowledgments

- Django Documentation
- Django REST Framework
- PostgreSQL Documentation
- JWT Authentication best practices

## 📞 Support

For support, email support@prodevjobboard.com or open an issue on GitHub.
