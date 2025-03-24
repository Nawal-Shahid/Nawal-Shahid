import os
import math
import numpy as np
from datetime import datetime, timedelta
from github import Github

# Beautiful pastel color palette
COLORS = {
    'background': '#F9F7F7',
    'ground': '#DBE2EF',
    'code': '#A6E3E9',
    'issues': '#FFC4C4',
    'reviews': '#C9B6E4',
    'text': '#3F3F44'
}

def get_contributions():
    g = Github(os.getenv('GH_TOKEN'))
    user = g.get_user(os.getenv('GITHUB_ACTOR'))
    events = user.get_public_events()
    
    counts = {'code': 0, 'issues': 0, 'reviews': 0}
    for event in events:
        if event.type in ['PushEvent', 'CreateEvent']:
            counts['code'] += 1
        elif event.type in ['IssuesEvent', 'IssueCommentEvent']:
            counts['issues'] += 1
        elif event.type in ['PullRequestReviewEvent', 'PullRequestReviewCommentEvent']:
            counts['reviews'] += 1
    return counts

def create_flower(x, y, color, size):
    petals = []
    for i in range(6):
        angle = math.radians(i * 60)
        px = x + (10 + size) * math.cos(angle)
        py = y + (10 + size) * math.sin(angle)
        petals.append(f'<circle cx="{px}" cy="{py}" r="{6 + size//2}" fill="{color}"/>')
    return f'''
    <rect x="{x-2}" y="{y+15}" width="4" height="20" fill="#A8D8B9"/>
    {''.join(petals)}
    <circle cx="{x}" cy="{y}" r="{5 + size//3}" fill="#FFEEAD"/>
    '''

def create_tree(x, y, size):
    return f'''
    <rect x="{x-3}" y="{y+10}" width="6" height="25" fill="#8B5A2B"/>
    <path d="M{x-15-size} {y-10-size} Q{x} {y-50-size*2} {x+15+size} {y-10-size} Z" fill="#A6E3E9"/>
    <circle cx="{x}" cy="{y-20-size}" r="{12+size}" fill="#A6E3E9"/>
    '''

def generate_svg(data):
    plants = []
    positions = set()
    
    # Create plants based on activity
    for i in range(min(10, data['code'])):
        x, y = np.random.randint(50, 350), np.random.randint(100, 180)
        plants.append(create_tree(x, y, i%3))
    
    for i in range(min(15, data['issues'])):
        x, y = np.random.randint(50, 350), np.random.randint(100, 180)
        plants.append(create_flower(x, y, COLORS['issues'], i%4))
    
    svg = f'''
    <svg width="400" height="250" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="{COLORS['background']}"/>
        <rect x="20" y="200" width="360" height="40" rx="10" fill="{COLORS['ground']}"/>
        
        <!-- Isometric grid lines -->
        <path d="M20 200 L380 200 L400 180 L40 180 Z" fill="none" stroke="#AAA" stroke-width="0.5" stroke-dasharray="5,5"/>
        
        {''.join(plants)}
        
        <!-- Legend -->
        <rect x="250" y="30" width="130" height="90" fill="white" fill-opacity="0.8" rx="5"/>
        <text x="315" y="50" text-anchor="middle" font-family="Arial" font-weight="bold">My Garden</text>
        <circle cx="265" cy="70" r="6" fill="{COLORS['code']}"/>
        <text x="280" y="74" font-family="Arial">Code: {data['code']}</text>
        <circle cx="265" cy="90" r="6" fill="{COLORS['issues']}"/>
        <text x="280" y="94" font-family="Arial">Issues: {data['issues']}</text>
        <circle cx="265" cy="110" r="6" fill="{COLORS['reviews']}"/>
        <text x="280" y="114" font-family="Arial">Reviews: {data['reviews']}</text>
    </svg>
    '''
    
    with open('README.md', 'w') as f:
        f.write(f'''# 🌸 My Beautiful GitHub Garden\n\n{svg}\n\n*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*''')

if __name__ == "__main__":
    data = get_contributions()
    generate_svg(data)
