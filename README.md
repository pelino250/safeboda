# SafeBoda

A Django-based ride-sharing platform similar to SafeBoda, designed to connect passengers with motorcycle taxi riders.

## Features

- **Custom User Authentication**: Email-based authentication system
- **User Types**: Support for two user types - Passengers and Riders
- **Phone Number Validation**: Integrated phone number validation with regex patterns
- **Admin Interface**: Django admin panel for user management
- **Environment Configuration**: Secure configuration using environment variables
- **Redis Caching**: High-performance caching for API endpoints using Redis
- **REST API**: Django REST Framework endpoints for users, passengers, and riders
- **Dummy Data Generation**: Management command to populate database with test data

## Requirements

- Python 3.8+
- Django 5.2.6
- SQLite (default database)
- Redis server (for caching)

## Dependencies

The project uses the following Python packages:

```
Django==5.2.6
djangorestframework==3.16.1
redis==5.0.1
django-redis==5.4.0
python-dotenv==1.1.1
pillow==11.3.0
asgiref==3.9.1
sqlparse==0.5.3
mypy==1.17.1
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd safeboda
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Redis Server**
   
   **On macOS (using Homebrew):**
   ```bash
   brew install redis
   brew services start redis
   ```
   
   **On Ubuntu/Debian:**
   ```bash
   sudo apt update
   sudo apt install redis-server
   sudo systemctl start redis-server
   sudo systemctl enable redis-server
   ```
   
   **On Windows:**
   Download and install Redis from the official website or use WSL.

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Environment Configuration**
   
   Copy the `.env` file and update the values:
   ```bash
   cp .env.example .env
   ```
   
   Update the following variables in your `.env` file:
   ```
   DJANGO_SECRET_KEY=your_actual_secret_key_here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a Superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Populate Database with Dummy Data (Optional)**
   
   To test the application with sample data and Redis caching functionality:
   ```bash
   python manage.py populate_dummy_data
   ```
   
   You can also specify custom counts:
   ```bash
   python manage.py populate_dummy_data --users 100 --passengers 60 --riders 40
   ```
   
   This will create:
   - Test users with realistic data
   - Passenger profiles with various preferences and locations
   - Rider profiles with different verification statuses and locations
   - Data suitable for testing Redis caching on the `/api/riders/available_riders/` endpoint

8. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

## Usage

### Accessing the Application

- **Development Server**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **API Root**: http://127.0.0.1:8000/api/

### API Endpoints

The application provides REST API endpoints for:

- **Users**: `/api/users/`
- **Passengers**: `/api/passengers/`
- **Riders**: `/api/riders/`

Key endpoints include:
- `GET /api/riders/available_riders/` - Get available riders (cached with Redis)
- `GET /api/passengers/my_profile/` - Get current user's passenger profile
- `GET /api/riders/my_profile/` - Get current user's rider profile
- `PATCH /api/riders/{id}/update_location/` - Update rider location

### User Types

The application supports two types of users:

1. **Passenger**: Users who request rides
2. **Rider**: Motorcycle taxi drivers who provide rides

### User Model

The custom user model includes:
- Email (used for authentication instead of username)
- User type (passenger/rider)
- Phone number with validation
- Standard Django user fields (first_name, last_name, etc.)

## Project Structure

```
safeboda/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .env                     # Environment variables
├── db.sqlite3              # SQLite database file
├── README.md               # This file
├── safeboda/               # Main project directory
│   ├── __init__.py
│   ├── settings.py         # Django settings
│   ├── urls.py            # URL configuration
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
└── users/                  # Users app
    ├── __init__.py
    ├── admin.py           # Admin configuration
    ├── apps.py            # App configuration
    ├── models.py          # User model definitions
    ├── tests.py           # Test cases
    ├── views.py           # View functions
    └── migrations/        # Database migrations
        ├── __init__.py
        └── 0001_initial.py
```

## Configuration

### Environment Variables

The application uses the following environment variables:

- `DJANGO_SECRET_KEY`: Secret key for Django security
- `DEBUG`: Debug mode (True/False)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

### Database

The project is configured to use SQLite by default. The database file `db.sqlite3` will be created in the project root after running migrations.

### Redis Caching

The application implements Redis caching for improved performance:

- **Cache Backend**: django-redis with Redis server
- **Cache Location**: `redis://127.0.0.1:6379/1`
- **Cached Endpoints**: 
  - `/api/riders/available_riders/` - Cached for 5 minutes (300 seconds)
- **Cache Invalidation**: Automatic cache clearing when rider location is updated
- **Benefits**: Reduces database queries for frequently accessed data

To verify Redis is working:
```bash
# Check if Redis is running
redis-cli ping
# Should return "PONG"

# Monitor cache operations (optional)
redis-cli monitor
```

## Development

### Running Tests

```bash
python manage.py test
```

### Making Database Changes

1. After modifying models, create migrations:
   ```bash
   python manage.py makemigrations
   ```

2. Apply migrations:
   ```bash
   python manage.py migrate
   ```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support or questions, please contact the development team or create an issue in the repository.