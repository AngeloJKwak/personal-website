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

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page route"""
    if request.method == 'POST':
        # Handle form submission
        return render_template('contact.html', success=True)
    return render_template('contact.html')

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


