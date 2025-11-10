from flask import Flask, render_template
from projects_data import PROJECTS

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'

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

@app.errorhandler(500)
def internal_server_error(e):
    """500 error handler"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)