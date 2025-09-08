# SafeBoda

A Django-based ride-sharing platform similar to SafeBoda, designed to connect passengers with motorcycle taxi riders.

## Features

- **Custom User Authentication**: Email-based authentication system
- **User Types**: Support for two user types - Passengers and Riders
- **Phone Number Validation**: Integrated phone number validation with regex patterns
- **Admin Interface**: Django admin panel for user management
- **Environment Configuration**: Secure configuration using environment variables

## Requirements

- Python 3.8+
- Django 5.2.6
- SQLite (default database)

## Dependencies

The project uses the following Python packages:

```
Django==5.2.6
python-dotenv==1.1.1
asgiref==3.9.1
sqlparse==0.5.3
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

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   
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

7. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

## Usage

### Accessing the Application

- **Development Server**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

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