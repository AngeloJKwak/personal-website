# Personal Portfolio Website

A clean, modern portfolio website built with Flask and Tailwind CSS.

## Features

- Responsive design that works on all devices
- Modern UI with Tailwind CSS
- Fast and lightweight
- Easy to customize
- SEO-friendly structure

## Local Development

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository
```bash
git clone <your-repo-url>
cd portfolio-website
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the development server
```bash
python app.py
```

5. Open your browser and visit `http://localhost:5000`

## Customization

### Update Your Information

1. **Personal Details**: Edit the following files to add your information:
   - `templates/base.html` - Update name, social links, email
   - `templates/index.html` - Update hero section, skills, projects
   - `templates/about.html` - Add your story and background
   - `templates/projects.html` - Showcase your projects

2. **Profile Photo**: Replace the SVG placeholder in `index.html` with:
   ```html
   <img src="{{ url_for('static', filename='images/profile.jpg') }}" 
        alt="Your Name" 
        class="w-64 h-64 md:w-80 md:h-80 rounded-full shadow-2xl object-cover">
   ```
   Then add your photo to `static/images/profile.jpg`

3. **Colors**: The site uses blue as the primary color. To change it:
   - Find and replace `blue-` with your preferred color (e.g., `green-`, `purple-`)
   - Update gradient colors in the hero and project cards

### Adding New Pages

1. Create a new HTML file in `templates/`
2. Add a route in `app.py`:
```python
@app.route('/new-page')
def new_page():
    return render_template('new-page.html')
```
3. Add a navigation link in `templates/base.html`

## Project Structure

```
portfolio-website/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── static/
│   ├── css/
│   │   └── style.css     # Custom CSS
│   ├── js/
│   │   └── main.js       # JavaScript for interactivity
│   └── images/           # Your images go here
└── templates/
    ├── base.html         # Base template
    ├── index.html        # Homepage
    ├── about.html        # About page
    └── projects.html     # Projects page
```

## Deployment

See the main deployment guide for instructions on deploying to Digital Ocean.

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Deployment**: Gunicorn, Nginx
- **Server**: Digital Ocean Ubuntu Droplet

## License

MIT License - Feel free to use this template for your own portfolio!

## Support

If you have questions or run into issues, feel free to open an issue on GitHub.