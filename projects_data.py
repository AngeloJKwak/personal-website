"""
Portfolio Projects Data

This file contains all project information for the portfolio website.
Edit this file to add, update, or remove projects.

Each project is a dictionary with the following structure:
- id: Unique identifier (lowercase, no spaces)
- name: Display name
- tagline: Optional subtitle
- description_short: Brief description for grid cards
- description_long: Detailed description for featured section (optional)
- features: List of key features (optional, for featured projects)
- technologies: List of technologies used
- categories: List of categories for filtering
- color: Theme color (blue, purple, green, orange, pink, teal, indigo, red)
- image: Image filename (must be in static/images/)
- image_type: 'logo' or 'screenshot'
- links: Dictionary of project links (use None if not available)
- featured: True/False - only one project should be featured
- order: Display order (lower numbers appear first)
"""

PROJECTS = [
    {
        'id': 'mrparty',
        'name': 'Mr. Party',
        'tagline': 'Making Music Social',
        'description_short': 'iOS app that lets users connect Spotify or Apple Music accounts and democratically vote on songs for events, creating collaborative playlists for any social gathering.',
        'description_long': 'An iOS mobile application that revolutionizes social music experiences. Mr. Party allows users to connect their Spotify or Apple Music accounts and create collaborative events where participants can democratically vote on the next song to be played, creating the perfect soundtrack for any gathering.',
        'features': [
            'Spotify & Apple Music integration for seamless connectivity',
            'Real-time democratic voting system for song selection',
            'Event creation and management for social gatherings',
            'Cloud-synced data with Firebase NoSQL database'
        ],
        'technologies': ['Swift', 'Xcode', 'Firebase', 'iOS', 'Spotify API', 'Apple Music API'],
        'categories': ['mobile'],
        'color': 'orange',
        'image': 'mrparty-logo.png',
        'image_type': 'logo',
        'links': {
            'website': 'https://www.mrpartyapp.com/',
            'demo': None,
            'github': None,
            'appstore': 'https://apps.apple.com/us/app/mr-party/id1213486893',
        },
        'featured': True,
        'order': 1
    },
    {
    'id': 'about-me-chatbot',
    'name': 'Professionally You AI Chatbot',
    'tagline': 'Talk to me! Well, an AI version of me...',  # Optional
    'description_short': 'AI Chatbot that can answer questions about my background and experience',
    'description_long': 'AI Chatbot that can answer questions about my background and experience',
    'technologies': ['Python', 'OpenAI', 'Gradio', 'Hugging Face'],
    'categories': ['web', 'python', 'ai'],
    'color': 'blue',  # blue, purple, green, orange, pink, teal, indigo, red
    'image': 'project.png',  # Put image in static/images/
    'image_type': 'logo',  # or 'screenshot'
    'links': {
        'website': 'https://www.udemy.com/course/the-complete-agentic-ai-engineering-course/',  # or None
        'demo': None,
        'github': 'https://github.com/...',  # or None
        'appstore': None,
    },
    'featured': False,  # Only ONE project should be True
    'order': 2,  # Lower numbers appear first
},
    
    # Add more projects below this line
    # Copy the template from QUICK_ADD_PROJECT.md
    
]

# Optional: Category display names (customize how categories appear in filters)
CATEGORY_NAMES = {
    'web': 'Web Development',
    'mobile': 'Mobile Apps',
    'python': 'Python',
    'data': 'Data & Analytics',
    'automation': 'Automation',
    'machine_learning': 'Machine Learning',
}

# Optional: Color schemes for easy reference
AVAILABLE_COLORS = [
    'blue',      # Professional, tech-focused
    'purple',    # Creative, modern
    'green',     # Growth, environmental
    'orange',    # Energetic, social
    'pink',      # Design, creative
    'teal',      # Clean, medical/health
    'indigo',    # Deep, enterprise
    'red',       # Urgent, important
]
