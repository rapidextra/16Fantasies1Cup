#!/usr/bin/env python3
"""
Setup script for 16 Fantasies 1 Cup
Helps configure the system for first-time use
"""

import os
import json
import sys
from pathlib import Path

def create_directories():
    """Create necessary directories"""
    directories = [
        'data',
        'data/teams', 
        'data/weekly',
        'data/historical',
        'Images'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def create_initial_data_files():
    """Create initial data files"""
    from config import Config
    
    # Create season-stats.json
    season_stats = {
        "currentWeek": 1,
        "totalWeeks": 17,
        "lastUpdated": "2025-01-01T00:00:00Z",
        "leagueInfo": Config.get_team_config()["league_info"],
        "topPerformers": {
            "highestScorer": {"team": "JewTeam", "points": 0, "week": 0},
            "mostConsistent": {"team": "JewTeam", "stdDev": 0},
            "worstBeat": {"team": "JewTeam", "points": 0, "week": 0}
        },
        "standings": [],
        "weeklyHighlights": [],
        "divisionStandings": {
            "FLO": [],
            "BTK": []
        },
        "recentActivity": {
            "trades": [],
            "waivers": []
        }
    }
    
    with open('data/season-stats.json', 'w') as f:
        json.dump(season_stats, f, indent=2)
    print("✅ Created data/season-stats.json")
    
    # Create weeks.js
    weeks_js = """window.CUP_WEEKS = [
  {
    week: 1,
    slug: 'week-01',
    title: 'The Big Kick-Off',
    blurb: 'Standings, trades, waivers, and matchup autopsies for the first week of the season.'
  }
];"""
    
    with open('weeks.js', 'w') as f:
        f.write(weeks_js)
    print("✅ Created weeks.js")

def setup_kaggle_config():
    """Help user set up Kaggle configuration"""
    print("\n🔧 Kaggle API Setup")
    print("To use real data from Kaggle, you'll need to:")
    print("1. Go to https://kaggle.com/account")
    print("2. Click 'Create New API Token'")
    print("3. Download the kaggle.json file")
    print("4. Set environment variables:")
    print("   export KAGGLE_USERNAME='your-username'")
    print("   export KAGGLE_KEY='your-api-key'")
    print("5. Update config.py with your dataset name")
    
    # Check if already configured
    if os.getenv('KAGGLE_USERNAME') and os.getenv('KAGGLE_KEY'):
        print("✅ Kaggle credentials found in environment variables")
    else:
        print("⚠️  Kaggle credentials not found - will use mock data")

def create_sample_team_files():
    """Create sample team profile files"""
    from config import Config
    
    teams = Config.get_team_config()["teams"]
    
    for team in teams:
        team_file = f"data/teams/{team['team'].lower()}.json"
        team_data = {
            "teamInfo": {
                "teamName": team["team"],
                "ownerName": team["owner"],
                "division": team["division"],
                "teamSlug": team["team"].lower(),
                "founded": 2024,
                "motto": f"Built for {team['division']} dominance"
            },
            "currentSeason": {
                "record": "0-0",
                "pointsFor": 0,
                "pointsAgainst": 0,
                "rank": 0,
                "lastUpdated": "2025-01-01T00:00:00Z"
            },
            "historicalData": {},
            "analytics": {
                "efficiency_rating": 0,
                "strength_of_schedule": 0,
                "playoff_odds": 0,
                "power_ranking": 0,
                "trends": {
                    "scoring_trend": "Unknown",
                    "consistency": "Unknown", 
                    "recent_form": "Unknown"
                }
            },
            "roastingMaterial": {
                "currentSeason": [],
                "historicalShame": [],
                "signatures": []
            },
            "headToHead": {}
        }
        
        with open(team_file, 'w') as f:
            json.dump(team_data, f, indent=2)
    
    print(f"✅ Created {len(teams)} team profile files")

def test_system():
    """Test the system setup"""
    print("\n🧪 Testing System Setup")
    
    try:
        # Test data fetcher
        sys.path.append('.')
        from scripts.fetch_kaggle_data import FantasyDataFetcher
        
        fetcher = FantasyDataFetcher()
        weekly_data = fetcher.fetch_weekly_data(1)
        
        if weekly_data and len(weekly_data.get('standings', [])) > 0:
            print("✅ Data fetcher working correctly")
            print(f"   Generated {len(weekly_data['standings'])} team standings")
        else:
            print("❌ Data fetcher not working correctly")
            
    except Exception as e:
        print(f"❌ Error testing system: {e}")

def main():
    """Main setup function"""
    print("🏈 16 Fantasies 1 Cup - Setup Script")
    print("=" * 40)
    
    # Create directories
    print("\n📁 Creating directories...")
    create_directories()
    
    # Create initial data files
    print("\n📄 Creating initial data files...")
    create_initial_data_files()
    
    # Create team files
    print("\n👥 Creating team profile files...")
    create_sample_team_files()
    
    # Setup Kaggle
    print("\n🔧 Setting up Kaggle integration...")
    setup_kaggle_config()
    
    # Test system
    print("\n🧪 Testing system...")
    test_system()
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Update config.py with your Kaggle dataset name")
    print("2. Set up Kaggle API credentials")
    print("3. Run: python scripts/fetch_kaggle_data.py --week 1")
    print("4. Run: python scripts/generate_newsletter.py --week 1")

if __name__ == "__main__":
    main()
