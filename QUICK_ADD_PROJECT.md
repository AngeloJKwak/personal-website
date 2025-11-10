# Quick Reference: Adding a Project

## Copy This Template into `projects_data.py` → `PROJECTS` list:

```python
{
    'id': 'my-project',
    'name': 'My Project Name',
    'tagline': 'Short catchy phrase',  # Optional
    'description_short': 'Brief description (2-3 sentences) shown on grid cards.',
    'description_long': 'Longer detailed description for featured section.',  # Optional
    'features': [  # Optional - only shows for featured projects
        'Feature 1',
        'Feature 2',
        'Feature 3'
    ],
    'technologies': ['Python', 'Flask', 'React'],
    'categories': ['web', 'python'],
    'color': 'blue',  # blue, purple, green, orange, pink, teal, indigo, red
    'image': 'project.png',  # Put image in static/images/
    'image_type': 'logo',  # or 'screenshot'
    'links': {
        'website': 'https://...',  # or None
        'demo': None,
        'github': 'https://github.com/...',  # or None
        'appstore': None,
    },
    'featured': False,  # Only ONE project should be True
    'order': 2,  # Lower numbers appear first
},
```

## That's It!

Save `projects_data.py` and your project appears:
- ✅ On projects page
- ✅ In filters automatically  
- ✅ On homepage (if featured)
- ✅ Everywhere with consistent styling

No HTML editing needed! 🎉

## File Structure

```
portfolio-website/
├── app.py                    # Main Flask app (don't edit for projects)
├── projects_data.py          # ← EDIT THIS FILE to manage projects
├── templates/
│   ├── projects.html
│   └── project_macros.html
└── static/
    └── images/               # Put project images here
```