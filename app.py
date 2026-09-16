from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_mail import Mail, Message
from projects_data import PROJECTS
import os
import re
import socket
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here-change-in-production')

# Email configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', '')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', '')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', '')

mail = Mail(app)

@app.route('/')
def home():
    """Homepage route"""
    # Get featured projects for homepage, or top 3 by order if not enough featured
    featured_projects = [p for p in PROJECTS if p.get('featured', False)]
    
    # If less than 3 featured, add more from top projects
    if len(featured_projects) < 3:
        all_projects_sorted = sorted(PROJECTS, key=lambda x: x.get('order', 999))
        for project in all_projects_sorted:
            if project not in featured_projects and len(featured_projects) < 3:
                featured_projects.append(project)
    
    # Limit to 3 projects max
    featured_projects = featured_projects[:3]
    
    return render_template('index.html', featured_projects=featured_projects)

@app.route('/about')
def about():
    """About page route"""
    return render_template('about.html')

@app.route('/resume-bot')
def resume_bot():
    """AI Resume Bot dedicated page"""
    return render_template('resume_bot.html')

@app.route('/projects')
def projects():
    """Projects page route"""
    # Get the featured project (first one marked as featured)
    featured = next((p for p in PROJECTS if p.get('featured', False)), None)
    
    # Get all projects sorted by order
    all_projects = sorted(PROJECTS, key=lambda x: x.get('order', 999))
    
    # Get unique categories for filters
    categories = set()
    for project in PROJECTS:
        categories.update(project.get('categories', []))
    
    return render_template('projects.html', 
                         featured_project=featured,
                         projects=all_projects,
                         categories=sorted(categories))

EMAIL_RE = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact form endpoint. The form itself lives on the homepage."""
    if request.method == 'GET':
        return redirect(url_for('home', _anchor='contact'))

    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    email = (data.get('email') or '').strip()
    message = (data.get('message') or '').strip()

    if not name or not email or not message:
        return jsonify({'error': 'Please fill in all fields.'}), 400
    if not EMAIL_RE.match(email):
        return jsonify({'error': 'Please enter a valid email address.'}), 400

    recipient = os.getenv('RECIPIENT_EMAIL') or app.config['MAIL_DEFAULT_SENDER']
    if not recipient or not app.config['MAIL_USERNAME']:
        app.logger.error('Contact form submitted but mail is not configured (missing MAIL_USERNAME/RECIPIENT_EMAIL).')
        return jsonify({'error': 'Message could not be sent right now. Please email me directly.'}), 503

    msg = Message(
        subject=f'Portfolio contact from {name}',
        recipients=[recipient],
        reply_to=email,
        body=f'From: {name} <{email}>\n\n{message}'
    )

    # smtplib has no timeout by default, so a blocked/unreachable SMTP port
    # hangs the request until the reverse proxy kills it. Bound it here so
    # we fail fast with a real JSON error instead.
    previous_timeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(8)
    try:
        mail.send(msg)
    except (socket.timeout, TimeoutError, ConnectionError, OSError):
        app.logger.exception('Timed out or failed connecting to the mail server')
        return jsonify({'error': "Message couldn't be sent (mail server unreachable). Please email me directly."}), 502
    except Exception:
        app.logger.exception('Failed to send contact form email')
        return jsonify({'error': 'Message could not be sent right now. Please try again later.'}), 500
    finally:
        socket.setdefaulttimeout(previous_timeout)

    return jsonify({'success': True, 'message': "Thanks for reaching out! I'll get back to you soon."})

@app.route('/app/<app_id>')
def embedded_app(app_id):
    """Route for embedded Hugging Face apps - pulls from projects_data.py"""
    # Find the project with matching ID
    project = next((p for p in PROJECTS if p.get('id') == app_id), None)
    
    if not project or 'huggingface_space' not in project:
        # If 404.html doesn't exist, return simple error
        try:
            return render_template('404.html'), 404
        except:
            return '<h1>404 - App Not Found</h1>', 404
    
    return render_template('app_embed.html',
                         app_name=project['name'],
                         app_description=project.get('description_long') or project['description_short'],
                         huggingface_url=project['huggingface_space'],
                         app_github=project['links'].get('github'))

@app.errorhandler(404)
def page_not_found(e):
    """404 error handler"""
    try:
        return render_template('404.html'), 404
    except:
        return '<h1>404 - Page Not Found</h1>', 404

@app.errorhandler(500)
def internal_server_error(e):
    """500 error handler"""
    try:
        return render_template('500.html'), 500
    except:
        return '<h1>500 - Server Error</h1>', 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


