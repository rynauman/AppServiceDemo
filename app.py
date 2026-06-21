import logging 
from azure.monitor.opentelemetry import configure_azure_monitor
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from email_validator import validate_email, EmailNotValidError
import os

# Configure OpenTelemetry to use Azure Monitor with the
# APPLICATIONINSIGHTS_CONNECTION_STRING environment variable.
configure_azure_monitor(
    logger_name="__name__",  # Set the namespace for the logger in which you would like to collect telemetry for if you are collecting logging telemetry. This is imperative so you do not collect logging telemetry from the SDK itself.
)
logger = logging.getLogger("__name__")  # Logging telemetry will be collected from logging calls made with this logger and all of it's children loggers.


app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///newsletter.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')


# Initialize database
db = SQLAlchemy(app)

# Database model for newsletter subscribers
class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=True)
    interests = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f'<Subscriber {self.email}>'


# Create tables
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    """Display the homepage with newsletter signup form."""
    return render_template('index.html')


@app.route('/subscribe', methods=['POST'])
def subscribe():
    """Handle newsletter subscription form submission."""
    try:
        # Get form data
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        interests = request.form.get('interests', '').strip()

        # Validate required fields
        if not all([first_name, last_name, email]):
            flash('Please fill in all required fields (first name, last name, email).', 'error')
            return redirect(url_for('index'))

        # Validate email format
        try:
            valid_email = validate_email(email)
            email = valid_email.email
        except EmailNotValidError as e:
            flash(f'Invalid email address: {str(e)}', 'error')
            return redirect(url_for('index'))

        # Check if subscriber already exists
        existing = Subscriber.query.filter_by(email=email).first()
        if existing:
            flash('This email is already subscribed to our newsletter.', 'warning')
            return redirect(url_for('index'))

        # Create new subscriber
        subscriber = Subscriber(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            interests=interests
        )

        db.session.add(subscriber)
        db.session.commit()

        flash(f'Welcome {first_name}! You have successfully subscribed to our newsletter.', 'success')
        return redirect(url_for('index'))

    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/subscribers')
def subscribers():
    """Display all newsletter subscribers (admin view)."""
    all_subscribers = Subscriber.query.order_by(Subscriber.created_at.desc()).all()
    count = len(all_subscribers)
    return render_template('subscribers.html', subscribers=all_subscribers, count=count)


@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors."""
    db.session.rollback()
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
