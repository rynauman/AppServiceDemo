# Newsletter Signup Web Application

A Python Flask web application that allows users to submit their personal information to subscribe to a newsletter. This application includes a clean, modern UI and a database to store subscriber information.

## Features

- **User-friendly signup form** - Collect first name, last name, email, phone, and interests
- **Email validation** - Ensures valid email addresses are stored
- **Duplicate prevention** - Prevents duplicate email subscriptions
- **Admin view** - View all subscribers with their information and signup dates
- **Responsive design** - Works seamlessly on desktop and mobile devices
- **Database storage** - SQLite database for storing subscriber information (can be configured for other databases)
- **Error handling** - Comprehensive error handling with user-friendly messages

## Requirements

- Python 3.8+
- Flask
- Flask-SQLAlchemy
- email-validator

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/rynauman/AppServiceDemo.git
   cd AppServiceDemo
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

## Running the Application

1. **Start the Flask development server**
   ```bash
   python app.py
   ```

2. **Open your browser and navigate to**
   ```
   http://localhost:5000
   ```

## Usage

### Subscribe to Newsletter
1. Go to the home page
2. Fill in your personal information:
   - First Name (required)
   - Last Name (required)
   - Email (required)
   - Phone (optional)
   - Interests (optional)
3. Click "Subscribe Now"
4. You'll receive a confirmation message

### View Subscribers (Admin)
- Click "View Subscribers" to see all newsletter subscribers
- The page displays subscriber count and a table with all subscriber details

## Project Structure

```
AppServiceDemo/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   ├── base.html         # Base template with styling
│   ├── index.html        # Signup form page
│   ├── subscribers.html  # Subscribers admin view
│   ├── 404.html          # 404 error page
│   └── 500.html          # 500 error page
└── README.md             # This file
```

## Environment Variables

You can configure the application using environment variables:

- `DATABASE_URL` - Database connection string (defaults to SQLite: `sqlite:///newsletter.db`)
- `SECRET_KEY` - Flask secret key for sessions (defaults to `dev-key-change-in-production`)
- `FLASK_ENV` - Set to `production` for production deployment

Example:
```bash
export DATABASE_URL="postgresql://user:password@localhost/newsletter"
export SECRET_KEY="your-secret-key-here"
python app.py
```

## Database

The application uses SQLAlchemy ORM with SQLite by default. The database is automatically created on first run.

### Subscriber Model

```
- id: Integer (Primary Key)
- first_name: String(100)
- last_name: String(100)
- email: String(120) - Unique
- phone: String(20) - Optional
- interests: String(255) - Optional
- created_at: DateTime - Auto-populated
```

## Deployment

### Azure App Service

1. Create an Azure App Service (Python 3.9+)
2. Set environment variables in Azure Portal:
   - `DATABASE_URL` (if using external database)
   - `SECRET_KEY`
3. Deploy using Git or ZIP upload

### Heroku

```bash
heroku create your-app-name
git push heroku main
```

### Docker

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

## Security Considerations

- Change the `SECRET_KEY` in production
- Use HTTPS in production
- Validate and sanitize all user inputs
- Store sensitive information securely
- Use environment variables for configuration
- Implement rate limiting for production
- Consider adding CSRF protection for production

## Future Enhancements

- User authentication and password reset
- Email confirmation for subscriptions
- Unsubscribe functionality
- Newsletter delivery integration
- Search and filter subscribers
- Export subscriber data to CSV
- Subscription preference management
- Analytics and reporting

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please create an issue in the repository.
