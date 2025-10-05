#!/usr/bin/env python3
"""
Configuration file for 16 Fantasies 1 Cup
Centralized configuration for easy customization
"""

import os
from typing import Dict, Any

class Config:
    """Configuration settings for the fantasy football newsletter system"""
    
    # League Information
    LEAGUE_NAME = "16 Fantasies 1 Cup"
    SEASON = 2025
    TOTAL_TEAMS = 16
    PLAYOFF_TEAMS = 8
    REGULAR_SEASON_WEEKS = 14
    
    # Data Sources
    KAGGLE_DATASET = "jgade/16-fantasies-1-cup"
    KAGGLE_USERNAME = os.getenv('KAGGLE_USERNAME', '')
    KAGGLE_KEY = os.getenv('KAGGLE_KEY', '')
    
    # File Paths
    DATA_DIR = "data"
    TEAMS_DIR = "data/teams"
    WEEKLY_DIR = "data/weekly"
    HISTORICAL_DIR = "data/historical"
    
    # Newsletter Settings
    DEFAULT_WEEK_TITLES = [
        "Judgment Day",
        "Trade Deadline Chaos", 
        "Playoff Push",
        "Do or Die",
        "Championship Chase",
        "Upset Special",
        "Rivalry Week",
        "Breakdown Boulevard",
        "Reality Check",
        "Crunch Time",
        "The Reckoning",
        "Destiny Calls"
    ]
    
    # Team Divisions
    DIVISIONS = {
        "FLO": "Finkle Laces Out",
        "BTK": "Bend the Knee"
    }
    
    # Roasting Content
    ROASTING_CATEGORIES = {
        "contender": [
            "Sitting pretty at the top, but can you handle the pressure?",
            "Leading the league while playing the easiest schedule - impressive or lucky?",
            "Great record, but playoff time is when boys become men.",
        ],
        "bubble": [
            "Fighting for that last playoff spot like it's Black Friday.",
            "One week you're hot, next week you're not. Make up your mind!",
            "Playoff hopes hanging by a thread thinner than your roster depth.",
        ],
        "pretender": [
            "A win is a win, but that score won't cut it most weeks.",
            "Benefitted from playing the worst team in the league. A flattering record.",
            "Alarm bells ringing - this team is in trouble.",
        ],
        "basement": [
            "Started the season right where they left off. In the bin.",
            "A shocking performance from a supposed contender. Awful start.",
            "The worst team in the league. A truly pathetic display.",
        ]
    }
    
    # Scoring Ranges for Mock Data
    SCORE_RANGES = {
        "excellent": (120, 180),
        "good": (100, 119),
        "average": (80, 99),
        "poor": (60, 79),
        "terrible": (0, 59)
    }
    
    # Transaction Probability (0.0 to 1.0)
    TRANSACTION_PROBABILITIES = {
        "trade": 0.3,  # 30% chance of trade per week
        "waiver": 0.7,  # 70% chance of waiver claim per week
    }
    
    @classmethod
    def get_team_config(cls) -> Dict[str, Any]:
        """Get team configuration"""
        return {
            "teams": [
                {"team": "JewTeam", "owner": "Jewish", "division": "FLO"},
                {"team": "gunga36", "owner": "King Gunga", "division": "BTK"},
                {"team": "Bonzo22", "owner": "Shane Train", "division": "FLO"},
                {"team": "healzyswarriors", "owner": "Healzy", "division": "BTK"},
                {"team": "FattyC26", "owner": "Fatty", "division": "FLO"},
                {"team": "MorgsLev13", "owner": "Morgs", "division": "FLO"},
                {"team": "coopersallstarz", "owner": "Coops", "division": "FLO"},
                {"team": "Stampy", "owner": "Stampy", "division": "FLO"},
                {"team": "3whits", "owner": "Whits", "division": "FLO"},
                {"team": "webbyt", "owner": "Webby", "division": "FLO"},
                {"team": "Wicka", "owner": "Wicka", "division": "FLO"},
                {"team": "5yearRebuild", "owner": "Joe", "division": "BTK"},
                {"team": "Sedgy", "owner": "Sedgy", "division": "FLO"},
                {"team": "Poddy", "owner": "Poddy", "division": "BTK"},
                {"team": "DaksDemons", "owner": "Dak", "division": "BTK"},
                {"team": "MickyMayn", "owner": "Mick", "division": "BTK"}
            ],
            "league_info": {
                "name": cls.LEAGUE_NAME,
                "season": cls.SEASON,
                "totalTeams": cls.TOTAL_TEAMS,
                "playoffTeams": cls.PLAYOFF_TEAMS,
                "regularSeasonWeeks": cls.REGULAR_SEASON_WEEKS
            }
        }
    
    @classmethod
    def is_kaggle_configured(cls) -> bool:
        """Check if Kaggle API is properly configured"""
        return bool(cls.KAGGLE_USERNAME and cls.KAGGLE_KEY)
    
    @classmethod
    def get_roast_for_category(cls, category: str, team_name: str = "") -> str:
        """Get a random roast for a team category"""
        import random
        roasts = cls.ROASTING_CATEGORIES.get(category, ["Performing as expected."])
        roast = random.choice(roasts)
        return roast.replace("{team}", team_name) if "{team}" in roast else roast
