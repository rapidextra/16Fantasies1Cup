#!/usr/bin/env python3
"""
Get upcoming matchups for pre-week newsletters
Works with existing data and can integrate with Sleeper API
"""

import os
import json
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime

class UpcomingMatchupsFetcher:
    def __init__(self, league_id: str = None):
        self.league_id = league_id or "your_league_id_here"
        self.data_dir = "data"
        
    def get_upcoming_matchups(self, week_number: int, method: str = "sleeper") -> List[Dict]:
        """
        Get upcoming matchups for a specific week
        
        Args:
            week_number: The week to get matchups for
            method: "sleeper", "standings", or "historical"
        """
        if method == "sleeper":
            return self._get_sleeper_matchups(week_number)
        elif method == "standings":
            return self._get_standings_based_matchups(week_number)
        elif method == "historical":
            return self._get_historical_matchups(week_number)
        else:
            raise ValueError("Method must be 'sleeper', 'standings', or 'historical'")
    
    def _get_sleeper_matchups(self, week_number: int) -> List[Dict]:
        """Get matchups from Sleeper API"""
        try:
            url = f"https://api.sleeper.app/v1/league/{self.league_id}/matchups/{week_number}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            matchups_data = response.json()
            return self._format_sleeper_matchups(matchups_data, week_number)
            
        except Exception as e:
            print(f"❌ Error fetching Sleeper matchups: {e}")
            print("🔄 Falling back to standings-based matchups...")
            return self._get_standings_based_matchups(week_number)
    
    def _format_sleeper_matchups(self, matchups_data: List[Dict], week_number: int) -> List[Dict]:
        """Format Sleeper API matchups data"""
        matchups = []
        
        # Group matchups by matchup_id
        matchup_groups = {}
        for matchup in matchups_data:
            matchup_id = matchup.get('matchup_id')
            if matchup_id not in matchup_groups:
                matchup_groups[matchup_id] = []
            matchup_groups[matchup_id].append(matchup)
        
        # Create matchup pairs
        for matchup_id, teams in matchup_groups.items():
            if len(teams) == 2:
                team1 = teams[0]
                team2 = teams[1]
                
                matchup = {
                    "week": week_number,
                    "team1": {
                        "owner": team1.get('owner', 'Unknown'),
                        "roster_id": team1.get('roster_id'),
                        "points": team1.get('points', 0),
                        "projected_points": team1.get('projected_points', 0)
                    },
                    "team2": {
                        "owner": team2.get('owner', 'Unknown'),
                        "roster_id": team2.get('roster_id'),
                        "points": team2.get('points', 0),
                        "projected_points": team2.get('projected_points', 0)
                    },
                    "matchup_id": matchup_id,
                    "status": "upcoming"
                }
                matchups.append(matchup)
        
        return matchups
    
    def _get_standings_based_matchups(self, week_number: int) -> List[Dict]:
        """Generate matchups based on current standings order"""
        standings = self._load_current_standings()
        if not standings:
            return []
        
        matchups = []
        
        # Create matchups based on standings order
        for i in range(0, len(standings), 2):
            if i + 1 < len(standings):
                team1 = standings[i]
                team2 = standings[i + 1]
                
                matchup = {
                    "week": week_number,
                    "team1": {
                        "owner": team1.get('owner', 'Unknown'),
                        "wins": team1.get('wins', 0),
                        "losses": team1.get('losses', 0),
                        "points_for": team1.get('points_for', 0)
                    },
                    "team2": {
                        "owner": team2.get('owner', 'Unknown'),
                        "wins": team2.get('wins', 0),
                        "losses": team2.get('losses', 0),
                        "points_for": team2.get('points_for', 0)
                    },
                    "matchup_id": f"week_{week_number}_matchup_{i//2 + 1}",
                    "status": "upcoming"
                }
                matchups.append(matchup)
        
        return matchups
    
    def _get_historical_matchups(self, week_number: int) -> List[Dict]:
        """Generate matchups based on historical patterns"""
        # This would use historical data to create more realistic matchups
        # For now, fall back to standings-based
        return self._get_standings_based_matchups(week_number)
    
    def _load_current_standings(self) -> List[Dict]:
        """Load current standings from weekly data"""
        # Try to find the latest weekly data
        latest_week = self._find_latest_weekly_data()
        if latest_week:
            weekly_file = os.path.join(self.data_dir, "weekly", f"week-{latest_week:02d}.json")
            if os.path.exists(weekly_file):
                with open(weekly_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('standings', [])
        
        # Fall back to season data
        season_file = os.path.join(self.data_dir, "season-stats.json")
        if os.path.exists(season_file):
            with open(season_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('standings', [])
        
        return []
    
    def _find_latest_weekly_data(self) -> Optional[int]:
        """Find the latest available weekly data"""
        weekly_dir = os.path.join(self.data_dir, "weekly")
        if not os.path.exists(weekly_dir):
            return None
        
        weeks = []
        for file in os.listdir(weekly_dir):
            if file.startswith("week-") and file.endswith(".json"):
                try:
                    week_num = int(file.split("-")[1].split(".")[0])
                    weeks.append(week_num)
                except ValueError:
                    continue
        
        return max(weeks) if weeks else None
    
    def save_upcoming_matchups(self, week_number: int, matchups: List[Dict]) -> str:
        """Save upcoming matchups to file"""
        output_file = os.path.join(self.data_dir, "weekly", f"upcoming-week-{week_number:02d}.json")
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        data = {
            "week": week_number,
            "season": 2025,
            "generated_at": datetime.now().isoformat(),
            "matchups": matchups
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Upcoming matchups saved to: {output_file}")
        return output_file

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Get upcoming matchups for pre-week newsletters')
    parser.add_argument('--week', type=int, required=True, help='Week number')
    parser.add_argument('--method', choices=['sleeper', 'standings', 'historical'], 
                       default='standings', help='Method to get matchups')
    parser.add_argument('--league-id', help='Sleeper league ID (required for sleeper method)')
    parser.add_argument('--save', action='store_true', help='Save matchups to file')
    
    args = parser.parse_args()
    
    fetcher = UpcomingMatchupsFetcher(args.league_id)
    matchups = fetcher.get_upcoming_matchups(args.week, args.method)
    
    print(f"📊 Found {len(matchups)} upcoming matchups for Week {args.week}")
    
    for i, matchup in enumerate(matchups, 1):
        team1 = matchup['team1']['owner']
        team2 = matchup['team2']['owner']
        print(f"  {i}. {team1} vs {team2}")
    
    if args.save:
        fetcher.save_upcoming_matchups(args.week, matchups)

if __name__ == "__main__":
    main()


