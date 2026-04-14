#!/usr/bin/env python3
"""
TrendPulse Task 1 - HackerNews Trending Stories
My first attempt at scraping HN API. Took me 3 hours debugging timeouts!
Written by John Doe - Dec 2024
"""

import requests
import json
import time
from datetime import datetime
import os

# HN API urls - no auth needed, yay!
TOP_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
STORY_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Gotta add this header or HN blocks you
HEADERS = {"User-Agent": "TrendPulse/1.0 (by John Doe)"}

# Keywords for categories - case doesn't matter
TECH_KEYWORDS = ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"]
NEWS_KEYWORDS = ["war", "government", "country", "president", "election", "climate", "attack", "global"]
SPORTS_KEYWORDS = ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"]
SCIENCE_KEYWORDS = ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"]
ENT_KEYWORDS = ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]

# Max 25 stories per category
MAX_PER_CAT = 25

def get_category(title):
    """Figure out what category this story belongs to. Returns None if no match."""
    if not title:
        return None
    
    title = title.lower()
    
    # Check tech first - most HN stories are tech
    for word in TECH_KEYWORDS:
        if word in title:
            return "technology"
    
    # Then news
    for word in NEWS_KEYWORDS:
        if word in title:
            return "worldnews"
    
    # Sports
    for word in SPORTS_KEYWORDS:
        if word in title:
            return "sports"
    
    # Science
    for word in SCIENCE_KEYWORDS:
        if word in title:
            return "science"
    
    # Entertainment last
    for word in ENT_KEYWORDS:
        if word in title:
            return "entertainment"
    
    return None  # Orphan story :(

def grab_top_ids():
    """Get top 500 story IDs from HN."""
    print(" Grabbing top 500 story IDs...")
    try:
        r = requests.get(TOP_URL, headers=HEADERS, timeout=15)
        r.raise_for_status()
        ids = r.json()
        print(f" Got {len(ids)} IDs, taking first 500")
        return ids[:500]
    except Exception as e:
        print(f" ERROR getting IDs: {e}")
        return []

def get_story(story_id):
    """Fetch one story. Skip if it fails."""
    try:
        url = STORY_URL.format(story_id)
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        return r.json()
    except:
        print(f"  Skip story {story_id} - failed")
        return None

def collect_all_stories(top_ids):
    """Main collection loop. Stop at 25 per category."""
    print(" Fetching stories...")
    
    stories = []
    counts = {
        "technology": 0, "worldnews": 0, "sports": 0, 
        "science": 0, "entertainment": 0
    }
    
    for i, story_id in enumerate(top_ids):
        # Stop if we have enough
        if all(counts[cat] >= MAX_PER_CAT for cat in counts):
            break
        
        story = get_story(story_id)
        if not story:
            continue
        
        # Need title and author
        if not story.get('title') or not story.get('by'):
            continue
        
        cat = get_category(story['title'])
        if cat and counts[cat] < MAX_PER_CAT:
            # Build the story dict
            new_story = {
                'post_id': story['id'],
                'title': story['title'],
                'category': cat,
                'score': story.get('score', 0),
                'num_comments': story.get('descendants', 0),
                'author': story['by'],
                'collected_at': datetime.now().isoformat()
            }
            stories.append(new_story)
            counts[cat] += 1
            
            if len(stories) % 20 == 0:
                print(f"   Got {len(stories)} stories so far...")
    
    print(" Collection done!")
    return stories

def save_json(stories):
    """Dump to data/ folder with today's date."""
    os.makedirs("data", exist_ok=True)
    
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"data/trends_{date_str}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(stories, f, indent=2, ensure_ascii=False)
    
    # Show breakdown
    cat_count = {}
    for s in stories:
        cat = s['category']
        cat_count[cat] = cat_count.get(cat, 0) + 1
    
    print(f"\n🎉 SAVED {len(stories)} stories to {filename}")
    print("Breakdown:")
    for cat, num in cat_count.items():
        print(f"  {cat}: {num}")

# MAIN
if __name__ == "__main__":
    print(" TrendPulse Task 1 - Let's collect some HN trends!")
    print("=" * 50)
    
    ids = grab_top_ids()
    if not ids:
        print(" No story IDs. Check internet?")
        exit(1)
    
    stories = collect_all_stories(ids)
    
    if stories:
        save_json(stories)
        print("\n Task 1 COMPLETE! Ready for Task 2!")
    else:
        print("No stories collected. Try again?")
