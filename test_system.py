#!/usr/bin/env python3
"""
Test script for 16 Fantasies 1 Cup
Quick test to verify the system is working correctly
"""

import sys
import os
import json
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from config import Config
        print("✅ Config module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import config: {e}")
        return False
    
    try:
        from scripts.fetch_kaggle_data import FantasyDataFetcher
        print("✅ Data fetcher imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import data fetcher: {e}")
        return False
    
    try:
        from scripts.generate_newsletter import NewsletterGenerator
        print("✅ Newsletter generator imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import newsletter generator: {e}")
        return False
    
    return True

def test_data_fetcher():
    """Test the data fetcher"""
    print("\n📊 Testing data fetcher...")
    
    try:
        from scripts.fetch_kaggle_data import FantasyDataFetcher
        
        fetcher = FantasyDataFetcher()
        weekly_data = fetcher.fetch_weekly_data(1)
        
        # Validate data structure
        required_fields = ['week', 'season', 'last_updated', 'matchups', 'standings', 'transactions']
        for field in required_fields:
            if field not in weekly_data:
                print(f"❌ Missing required field: {field}")
                return False
        
        if len(weekly_data['standings']) != 16:
            print(f"❌ Expected 16 teams, got {len(weekly_data['standings'])}")
            return False
        
        print("✅ Data fetcher working correctly")
        print(f"   Generated {len(weekly_data['standings'])} team standings")
        print(f"   Generated {len(weekly_data['matchups'])} matchups")
        return True
        
    except Exception as e:
        print(f"❌ Data fetcher test failed: {e}")
        return False

def test_newsletter_generator():
    """Test the newsletter generator"""
    print("\n📰 Testing newsletter generator...")
    
    try:
        from scripts.generate_newsletter import NewsletterGenerator
        
        generator = NewsletterGenerator()
        
        # Test with mock data
        test_data = {
            "week": 1,
            "season": 2025,
            "last_updated": "2025-01-01T00:00:00Z",
            "matchups": [
                {
                    "team1": "JewTeam",
                    "team2": "gunga36", 
                    "team1_score": 120.5,
                    "team2_score": 98.3,
                    "winner": "JewTeam"
                }
            ],
            "standings": [
                {
                    "rank": 1,
                    "team": "JewTeam",
                    "owner": "Jewish Lightning",
                    "record": "1-0",
                    "points_for": 120.5,
                    "points_against": 98.3,
                    "division": "FLO"
                }
            ],
            "transactions": {
                "trades": [],
                "waivers": []
            }
        }
        
        # This should not fail even if template doesn't exist
        print("✅ Newsletter generator initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Newsletter generator test failed: {e}")
        return False

def test_file_structure():
    """Test that required files exist"""
    print("\n📁 Testing file structure...")
    
    required_files = [
        'config.py',
        'scripts/fetch_kaggle_data.py',
        'scripts/generate_newsletter.py',
        'index.html',
        'weeks.js'
    ]
    
    required_dirs = [
        'data',
        'data/teams',
        'data/weekly',
        'Images'
    ]
    
    all_good = True
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ Missing: {file_path}")
            all_good = False
    
    for dir_path in required_dirs:
        if Path(dir_path).is_dir():
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ Missing directory: {dir_path}")
            all_good = False
    
    return all_good

def test_config():
    """Test configuration"""
    print("\n⚙️ Testing configuration...")
    
    try:
        from config import Config
        
        # Test basic config values
        assert Config.LEAGUE_NAME == "16 Fantasies 1 Cup"
        assert Config.TOTAL_TEAMS == 16
        assert Config.PLAYOFF_TEAMS == 8
        
        # Test team config
        team_config = Config.get_team_config()
        assert len(team_config['teams']) == 16
        
        print("✅ Configuration working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 16 Fantasies 1 Cup - System Test")
    print("=" * 40)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Configuration", test_config),
        ("Imports", test_imports),
        ("Data Fetcher", test_data_fetcher),
        ("Newsletter Generator", test_newsletter_generator)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} test failed")
    
    print(f"\n{'='*50}")
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        print("\nNext steps:")
        print("1. Run: python setup.py")
        print("2. Configure your Kaggle dataset in config.py")
        print("3. Run: python scripts/fetch_kaggle_data.py --week 1")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
