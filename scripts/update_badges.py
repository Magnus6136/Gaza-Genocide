#!/usr/bin/env python3
"""
Update README badges with latest statistics
"""

import json
import re
from datetime import datetime
import os

def load_latest_stats():
    """Load the latest statistics from JSON file"""
    try:
        with open('data/latest_stats.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("No statistics file found. Run fetch_statistics.py first.")
        return None
    except Exception as e:
        print(f"Error loading statistics: {e}")
        return None

def create_badge_url(label, value, color="red"):
    """Create a shields.io badge URL"""
    # Clean the value for URL encoding
    clean_value = str(value).replace('+', '%2B').replace(' ', '%20')
    clean_label = str(label).replace(' ', '%20')
    
    return f"https://img.shields.io/badge/{clean_label}-{clean_value}-{color}?style=for-the-badge"

def update_readme_badges():
    """Update the README.md file with new badge URLs"""
    stats = load_latest_stats()
    if not stats:
        return False
    
    # Read current README
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading README.md: {e}")
        return False
    
    # Create new badge URLs
    badges = {
        "Death Toll": create_badge_url("Death%20Toll", stats.get("total_deaths", "Loading..."), "red"),
        "Children Killed": create_badge_url("Children%20Killed", stats.get("children_deaths", "Loading..."), "orange"),
        "Women Killed": create_badge_url("Women%20Killed", stats.get("women_deaths", "Loading..."), "purple"),
        "Injured": create_badge_url("Injured", stats.get("total_injured", "Loading..."), "yellow"),
        "Displaced": create_badge_url("Displaced", stats.get("displaced_people", "Loading..."), "blue"),
        "Hospitals": create_badge_url("Hospitals%20Operational", stats.get("operational_hospitals", "Loading..."), "green"),
        "Last Updated": create_badge_url("Last%20Updated", stats.get("last_updated", "Loading..."), "blue")
    }
    
    # Update badge URLs in README
    for badge_name, new_url in badges.items():
        # Find and replace badge URLs
        pattern = rf'https://img\.shields\.io/badge/[^)]*{badge_name.replace(" ", "%20")}[^)]*'
        replacement = new_url
        
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    # Update the last updated timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M UTC")
    content = re.sub(
        r'\*\*Last Updated\*\*: .*',
        f'**Last Updated**: {timestamp}',
        content
    )
    
    # Write updated README
    try:
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"README badges updated successfully at {timestamp}")
        return True
    except Exception as e:
        print(f"Error writing README.md: {e}")
        return False

def create_api_endpoint():
    """Create a simple API endpoint file for badges"""
    stats = load_latest_stats()
    if not stats:
        return False
    
    # Create API endpoint for dynamic badges
    api_data = {
        "total_deaths": stats.get("total_deaths", "Loading..."),
        "children_deaths": stats.get("children_deaths", "Loading..."),
        "women_deaths": stats.get("women_deaths", "Loading..."),
        "total_injured": stats.get("total_injured", "Loading..."),
        "displaced_people": stats.get("displaced_people", "Loading..."),
        "operational_hospitals": stats.get("operational_hospitals", "Loading..."),
        "last_updated": stats.get("last_updated", "Loading..."),
        "fetch_timestamp": stats.get("fetch_timestamp", ""),
        "sources": stats.get("sources", [])
    }
    
    try:
        with open('data/api_stats.json', 'w', encoding='utf-8') as f:
            json.dump(api_data, f, indent=2, ensure_ascii=False)
        print("API endpoint created: data/api_stats.json")
        return True
    except Exception as e:
        print(f"Error creating API endpoint: {e}")
        return False

if __name__ == "__main__":
    print("Updating README badges...")
    success = update_readme_badges()
    
    if success:
        print("Creating API endpoint...")
        create_api_endpoint()
        print("Badge update completed successfully!")
    else:
        print("Badge update failed!") 