#!/usr/bin/env python3
"""
Additional code to add to your Kaggle notebook for pre-week newsletter data
Add this to the end of your notebook after the creative brief generation
"""

import random
from datetime import datetime, timedelta

def generate_preweek_data(week_number: int, standings_data: dict, matchups_data: list) -> dict:
    """
    Generate pre-week newsletter data based on current standings and matchups
    Add this function to your notebook
    """
    
    # 1. Generate upcoming matchups for next week
    upcoming_matchups = generate_upcoming_matchups(week_number + 1, standings_data)
    
    # 2. Generate player projections
    player_projections = generate_player_projections()
    
    # 3. Generate weather data
    weather_data = generate_weather_data()
    
    # 4. Generate injury reports
    injury_reports = generate_injury_reports()
    
    # 5. Generate storylines
    storylines = generate_storylines(standings_data, matchups_data)
    
    # 6. Generate waiver wire picks
    waiver_picks = generate_waiver_picks()
    
    return {
        "UpcomingMatchups": upcoming_matchups,
        "PlayerProjections": player_projections,
        "WeatherWatch": weather_data,
        "InjuryReport": injury_reports,
        "Storylines": storylines,
        "WaiverWire": waiver_picks
    }

def generate_upcoming_matchups(week: int, standings: dict) -> list:
    """Generate predicted matchups for next week"""
    matchups = []
    
    # Get current standings
    overall_standings = standings.get('Overall', [])
    
    # Create matchups based on current standings
    for i in range(0, len(overall_standings), 2):
        if i + 1 < len(overall_standings):
            team1 = overall_standings[i]
            team2 = overall_standings[i + 1]
            
            # Generate predicted scores based on current performance
            base_score1 = team1.get('PF', 0) / max(team1.get('Wins', 1), 1) + random.uniform(-10, 10)
            base_score2 = team2.get('PF', 0) / max(team2.get('Wins', 1), 1) + random.uniform(-10, 10)
            
            matchup = {
                "Week": week,
                "Team1": team1.get('Owner', ''),
                "Team2": team2.get('Owner', ''),
                "PredictedScore1": round(max(base_score1, 50), 1),
                "PredictedScore2": round(max(base_score2, 50), 1),
                "Confidence": random.choice(["High", "Medium", "Low"]),
                "KeyMatchup": random.choice([True, False]),
                "Margin": round(abs(base_score1 - base_score2), 1)
            }
            matchups.append(matchup)
    
    return matchups

def generate_player_projections() -> list:
    """Generate player projections for the week"""
    players = [
        {"Player": "Josh Allen (QB)", "Team": "Buffalo Bills", "ProjectedPoints": 24.5, "Matchup": "vs Miami", "Weather": "Clear"},
        {"Player": "Christian McCaffrey (RB)", "Team": "San Francisco 49ers", "ProjectedPoints": 18.2, "Matchup": "vs Arizona", "Weather": "Clear"},
        {"Player": "Tyreek Hill (WR)", "Team": "Miami Dolphins", "ProjectedPoints": 16.8, "Matchup": "at Buffalo", "Weather": "Snow"},
        {"Player": "Travis Kelce (TE)", "Team": "Kansas City Chiefs", "ProjectedPoints": 12.4, "Matchup": "vs Denver", "Weather": "Clear"},
        {"Player": "Justin Tucker (K)", "Team": "Baltimore Ravens", "ProjectedPoints": 9.1, "Matchup": "vs Cleveland", "Weather": "Wind"}
    ]
    
    return players

def generate_weather_data() -> list:
    """Generate weather impact data"""
    cities = ["Buffalo", "Green Bay", "Chicago", "Denver", "Cleveland", "Pittsburgh"]
    conditions = ["Snow", "Rain", "Wind", "Cold", "Heat", "Clear"]
    
    weather_data = []
    for _ in range(3):
        city = random.choice(cities)
        condition = random.choice(conditions)
        
        weather_data.append({
            "City": city,
            "Condition": condition,
            "Temperature": f"{random.randint(15, 85)}°F",
            "WindSpeed": f"{random.randint(5, 25)} mph",
            "Impact": get_weather_impact(condition),
            "GamesAffected": random.randint(1, 3)
        })
    
    return weather_data

def get_weather_impact(condition: str) -> str:
    """Get weather impact description"""
    impacts = {
        "Snow": "Favor running backs and defenses, avoid kickers",
        "Rain": "Slippery conditions favor ground game",
        "Wind": "Avoid passing games, kickers struggle",
        "Cold": "Ball handling issues, favor experienced players",
        "Heat": "Fatigue factor, favor deeper benches",
        "Clear": "Perfect conditions for all positions"
    }
    return impacts.get(condition, "Minimal impact expected")

def generate_injury_reports() -> list:
    """Generate injury report data"""
    injuries = [
        {"Player": "Christian McCaffrey", "Team": "San Francisco 49ers", "Status": "Questionable", "Injury": "Ankle", "Impact": "High", "News": "Limited in practice"},
        {"Player": "Travis Kelce", "Team": "Kansas City Chiefs", "Status": "Probable", "Injury": "Knee", "Impact": "Medium", "News": "Expected to play"},
        {"Player": "Tyreek Hill", "Team": "Miami Dolphins", "Status": "Doubtful", "Injury": "Hamstring", "Impact": "High", "News": "Did not practice"},
        {"Player": "Josh Allen", "Team": "Buffalo Bills", "Status": "Probable", "Injury": "Shoulder", "Impact": "Low", "News": "Full practice"},
        {"Player": "Justin Tucker", "Team": "Baltimore Ravens", "Status": "Questionable", "Injury": "Back", "Impact": "Low", "News": "Limited practice"}
    ]
    
    return random.sample(injuries, 3)

def generate_storylines(standings: dict, matchups: list) -> list:
    """Generate storylines based on current performance"""
    overall_standings = standings.get('Overall', [])
    
    storylines = []
    
    # Top team storylines
    if overall_standings:
        top_team = overall_standings[0]
        storylines.append(f"Can {top_team.get('Owner', 'Unknown')} maintain their perfect record?")
        
        # Winless team storylines
        winless_teams = [team for team in overall_standings if team.get('Wins', 0) == 0]
        if winless_teams:
            storylines.append(f"Will {winless_teams[0].get('Owner', 'Unknown')} finally get their first win?")
    
    # Division race storylines
    storylines.append("The division title race heats up as we enter the crucial mid-season stretch")
    storylines.append("Several teams are on the playoff bubble and need a big week")
    storylines.append("The waiver wire is heating up with several key pickups available")
    
    return storylines[:4]  # Return top 4 storylines

def generate_waiver_picks() -> list:
    """Generate waiver wire recommendations"""
    positions = ["QB", "RB", "WR", "TE", "K", "DEF"]
    players = [
        "Sleeper RB", "Backup QB", "Handcuff RB", "Streaming TE", 
        "Hot WR", "Rookie RB", "Veteran WR", "Kicker Stream"
    ]
    
    picks = []
    for _ in range(5):
        picks.append({
            "Player": random.choice(players),
            "Position": random.choice(positions),
            "Team": random.choice(["FA", "Waivers"]),
            "Reason": random.choice([
                "Favorable matchup this week",
                "Injury to starter opens opportunity",
                "Weather conditions favor this position",
                "Revenge game narrative",
                "Prime time performance incoming"
            ]),
            "FAABSuggestion": random.randint(5, 50)
        })
    
    return picks

# Example usage in your notebook:
# Add this to the end of your notebook after generating the creative brief

# Generate pre-week data
preweek_data = generate_preweek_data(WEEK_TO_ANALYZE + 1, creative_brief['Standings'], creative_brief['Matchups'])

# Add to your creative brief
creative_brief.update(preweek_data)

# Save the enhanced creative brief
enhanced_yaml = yaml.dump(creative_brief, sort_keys=False, indent=2)
with open(f"creative_brief_week{WEEK_TO_ANALYZE}_enhanced.yaml", "w") as f:
    f.write(enhanced_yaml)

print(f"✅ Enhanced creative brief saved with pre-week data!")


