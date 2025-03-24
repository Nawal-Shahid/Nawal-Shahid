import os
import math
import numpy as np
from datetime import datetime, timedelta
from github import Github
from dateutil.relativedelta import relativedelta

# Configuration
USERNAME = os.getenv('GITHUB_REPOSITORY_OWNER')
TOKEN = os.getenv('GH_TOKEN')

# Pastel color palette
COLORS = {
    'background': '#F8F9FA',
    'ground': '#E1F5E3',
    'grid': '#D1E7DD',
    'code': '#A8E6CF',
    'issues': '#FFD3B6',
    'reviews': '#D4A5C9',
    'water': '#B5EAD7',
    'text': '#555555'
}

def get_contribution_data():
    g = Github(TOKEN)
    user = g.get_user(USERNAME)
    
    # Get events from the last 90 days
    since = datetime.now() - timedelta(days=90)
    events = user.get_public_events()
    
    counts = {
        'code': 0,
        'issues': 0,
        'reviews': 0,
        'last_active': None
    }
    
    for event in events:
        if event.created_at < since:
            continue
            
        if counts['last_active'] is None or event.created_at > counts['last_active']:
            counts['last_active'] = event.created_at
            
        if event.type in ['PushEvent', 'CreateEvent']:
            counts['code'] += 1
        elif event.type in ['IssuesEvent', 'IssueCommentEvent']:
            counts['issues'] += 1
        elif event.type in ['PullRequestReviewEvent', 'PullRequestReviewCommentEvent']:
            counts['reviews'] += 1
    
    return counts

def generate_isometric_plant(x, y, plant_type, size):
    """Generate isometric 3D pixel art plant"""
    size = max(1, min(4, size))
    color = COLORS[plant_type]
    dark_color = adjust_color(color, -20)
    
    if plant_type == 'code':
        # Isometric tree
        return f'''
        <!-- Trunk -->
        <path d="M{x+10} {y+5} L{x+12} {y-5} L{x+14} {y+5} Z" fill="#8B5A2B"/>
        
        <!-- Leaves -->
        <rect x="{x+5}" y="{y-15}" width="{10+size*2}" height="{10+size*2}" 
              transform="skewX(-30)" fill="{color}"/>
        <rect x="{x+8}" y="{y-25}" width="{6+size*2}" height="{6+size*2}" 
              transform="skewX(-30)" fill="{dark_color}"/>
        '''
    elif plant_type == 'issues':
        # Isometric flower
        petals = []
        for i in range(6):
            angle = math.radians(i * 60)
            px = x + 10 + (8 + size) * math.cos(angle)
            py = y - 10 + (8 + size) * math.sin(angle) * 0.5
            petals.append(f'<circle cx="{px}" cy="{py}" r="{3 + size//2}" fill="{color}"/>')
        return f'''
        <!-- Stem -->
        <rect x="{x+9}" y="{y}" width="2" height="15" fill="#7CB342"/>
        
        <!-- Petals -->
        {''.join(petals)}
        
        <!-- Center -->
        <circle cx="{x+10}" cy="{y-10}" r="{3 + size//3}" fill="#FFEEAD"/>
        '''
    else:  # reviews
        # Isometric bush
        return f'''
        <rect x="{x}" y="{y}" width="{10 + size*3}" height="{6 + size}" 
              transform="skewX(-30)" fill="{color}"/>
        <rect x="{x+5}" y="{y-5}" width="{8 + size*2}" height="{5 + size}" 
              transform="skewX(-30)" fill="{dark_color}"/>
        '''

def adjust_color(hex_color, amount):
    """Lighten or darken a color"""
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    adjusted = [min(255, max(0, x + amount)) for x in rgb]
    return '#%02x%02x%02x' % tuple(adjusted)

def generate_svg(data):
    """Generate complete isometric garden SVG"""
    svg_width = 500
    svg_height = 300
    
    # Scale plant counts
    total = sum([data['code'], data['issues'], data['reviews']]) or 1
    code_count = min(10, math.ceil(data['code'] / total * 20))
    issue_count = min(10, math.ceil(data['issues'] / total * 20))
    review_count = min(10, math.ceil(data['reviews'] / total * 20))
    
    # Generate plant positions in isometric grid
    plants = []
    positions = set()
    
    def get_position():
        while True:
            x = np.random.randint(30, 400)
            y = np.random.randint(100, 220)
            # Simple check to prevent overlap
            if all(abs(x-px) + abs(y-py) > 30 for (px, py) in positions):
                positions.add((x, y))
                return x, y
    
    # Generate code plants (trees)
    for i in range(code_count):
        x, y = get_position()
        plants.append(generate_isometric_plant(x, y, 'code', i % 3 + 1))
    
    # Generate issue plants (flowers)
    for i in range(issue_count):
        x, y = get_position()
        plants.append(generate_isometric_plant(x, y, 'issues', i % 2 + 1))
    
    # Generate review plants (bushes)
    for i in range(review_count):
        x, y = get_position()
        plants.append(generate_isometric_plant(x, y, 'reviews', i % 4 + 1))
    
    # Generate watering can position
    days_inactive = (datetime.now() - data['last_active']).days if data['last_active'] else 99
    can_x = max(30, min(450, 50 + days_inactive * 4))
    
    svg = f'''
    <svg width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}" 
         xmlns="http://www.w3.org/2000/svg" style="background-color:{COLORS['background']}">
        <style>
            .text {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 12px; fill: {COLORS['text']}; }}
            .title {{ font-size: 16px; font-weight: 600; }}
        </style>
        
        <!-- Isometric ground -->
        <polygon points="0,250 500,250 450,200 50,200" fill="{COLORS['ground']}"/>
        <polygon points="50,200 450,200 400,150 100,150" fill="{COLORS['grid']}" opacity="0.2"/>
        
        <!-- Plants -->
        {''.join(plants)}
        
        <!-- Watering can -->
        <path d="M{can_x},210 L{can_x+15},200 L{can_x+20},205 L{can_x+5},215 Z" fill="{COLORS['water']}"/>
        <rect x="{can_x+15}" y="200" width="5" height="15" fill="{COLORS['water']}"/>
        
        <!-- Legend -->
        <rect x="350" y="30" width="140" height="100" fill="white" fill-opacity="0.8" rx="5"/>
        
        <text x="420" y="50" text-anchor="middle" class="title">My Garden</text>
        
        <circle cx="360" cy="70" r="6" fill="{COLORS['code']}"/>
        <text x="375" y="74" class="text">Code: {data['code']}</text>
        
        <circle cx="360" cy="90" r="6" fill="{COLORS['issues']}"/>
        <text x="375" y="94" class="text">Issues: {data['issues']}</text>
        
        <circle cx="360" cy="110" r="6" fill="{COLORS['reviews']}"/>
        <text x="375" y="114" class="text">Reviews: {data['reviews']}</text>
        
        <text x="360" cy="130" class="text" dy="4">Updated: {datetime.now().strftime('%Y-%m-%d')}</text>
    </svg>
    '''
    
    return svg

def update_readme(svg):
    with open('README.md', 'r+') as f:
        content = f.read()
        
        marker_start = "<!-- GARDEN_START -->"
        marker_end = "<!-- GARDEN_END -->"
        
        new_content = re.sub(
            f"{marker_start}.*?{marker_end}",
            f"{marker_start}\n{svg}\n{marker_end}",
            content,
            flags=re.DOTALL
        )
        
        f.seek(0)
        f.write(new_content)
        f.truncate()

if __name__ == "__main__":
    data = get_contribution_data()
    svg = generate_svg(data)
    update_readme(svg)
