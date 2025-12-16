from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
from projects_data import PROJECTS
import os
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

@app.errorhandler(404)
def page_not_found(e):
    """404 error handler"""
    return render_template('404.html'), 404

@app.route('/contact', methods=['POST'])
def contact():
    """Handle contact form submissions"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not all(k in data for k in ['name', 'email', 'message']):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        name = data['name']
        email = data['email']
        message = data['message']
        
        # Create email message
        msg = Message(
            subject=f'New Contact Form Submission from {name}',
            recipients=[os.getenv('RECIPIENT_EMAIL', 'angelokwak@gmail.com')],
            body=f'''
Name: {name}
Email: {email}

Message:
{message}
            ''',
            reply_to=email
        )
        
        # Send email
        mail.send(msg)
        
        return jsonify({'success': True, 'message': 'Thank you for your message! I\'ll get back to you soon.'}), 200
        
    except Exception as e:
        app.logger.error(f'Error sending email: {str(e)}')
        return jsonify({'success': False, 'error': 'Failed to send message. Please try again later.'}), 500

@app.errorhandler(500)
def internal_server_error(e):
    """500 error handler"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)