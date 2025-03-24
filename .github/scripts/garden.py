import os
from datetime import datetime

# Simple garden SVG
garden = f"""
<svg width="400" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#f0f8ff"/>
  <text x="50%" y="30" text-anchor="middle" font-family="Arial" font-size="20">
    {os.getenv('GITHUB_ACTOR')}'s Garden
  </text>
  <circle cx="100" cy="100" r="40" fill="#a8e6cf"/>
  <circle cx="200" cy="120" r="30" fill="#ffd3b6"/>
  <circle cx="300" cy="100" r="35" fill="#d4a5c9"/>
  <text x="50%" y="180" text-anchor="middle" font-family="Arial">
    Last updated: {datetime.now().strftime('%Y-%m-%d')}
  </text>
</svg>
"""

# Update README
with open('README.md', 'w') as f:
    f.write(f"# 🌿 My GitHub Garden\n\n{garden}\n\n*Updates daily*")
