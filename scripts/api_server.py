#!/usr/bin/env python3
"""
Simple API server for Gaza statistics
Can be deployed on platforms like Vercel, Netlify, or Heroku
"""

from flask import Flask, jsonify, send_from_directory
import json
import os
from datetime import datetime
from fetch_statistics import save_statistics

app = Flask(__name__)

@app.route('/')
def home():
    """Home endpoint with basic info"""
    return jsonify({
        "name": "Gaza Statistics API",
        "description": "Real-time statistics from verified sources",
        "endpoints": {
            "/stats": "Latest statistics",
            "/badges": "Badge-ready statistics",
            "/health": "API health check"
        },
        "last_updated": datetime.now().isoformat()
    })

@app.route('/stats')
def get_stats():
    """Get complete statistics"""
    try:
        # Update statistics first
        save_statistics()
        
        # Load and return latest stats
        with open('data/latest_stats.json', 'r', encoding='utf-8') as f:
            stats = json.load(f)
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/badges')
def get_badges():
    """Get statistics formatted for badges"""
    try:
        # Update statistics first
        save_statistics()
        
        # Load stats
        with open('data/latest_stats.json', 'r', encoding='utf-8') as f:
            stats = json.load(f)
        
        # Format for badges
        badge_stats = {
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
        
        return jsonify(badge_stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

@app.route('/data/<path:filename>')
def serve_data(filename):
    """Serve data files"""
    return send_from_directory('data', filename)

if __name__ == '__main__':
    # For local development
    app.run(debug=True, host='0.0.0.0', port=5000)
else:
    # For deployment (Vercel, Netlify, etc.)
    # This will be used by the deployment platform
    pass 