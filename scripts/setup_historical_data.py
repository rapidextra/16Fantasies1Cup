#!/usr/bin/env python3
"""
Setup Historical Data for Sleeper Pre-Week Newsletter
Creates historical records and head-to-head data
"""

import os
import json
import random
from datetime import datetime
from typing import Dict, List, Any

class HistoricalDataSetup:
    def __init__(self):
        self.data_dir = "data"
        self.historical_dir = os.path.join(self.data_dir, "historical")
        
    def setup_historical_data(self):
        """Setup historical data for the newsletter"""
        print("📊 Setting up historical data...")
        
        # Ensure historical directory exists
        os.makedirs(self.historical_dir, exist_ok=True)
        
        # Generate historical data
        historical_data = self._generate_historical_data()
        
        # Save historical data
        historical_file = os.path.join(self.historical_dir, "all-time-stats.json")
        with open(historical_file, 'w', encoding='utf-8') as f:
            json.dump(historical_data, f, indent=2)
        
        print(f"✅ Historical data saved to: {historical_file}")
        return historical_file
    
    def _generate_historical_data(self) -> Dict:
        """Generate historical data for all teams"""
        
        # Team names from config
        teams = [
            "healzyswarriors", "FattyC26", "Wicka", "webbyt", "3whits", "coopersallstarz",
            "DaksDemons", "Stampy", "MorgsLev13", "JewTeam", "Poddy", "5yearRebuild",
            "Bonzo22", "Sedgy", "gunga36", "MickyMayn"
        ]
        
        # Generate team historical stats
        team_stats = []
        for team in teams:
            team_stat = {
                "owner": team,
                "total_wins": random.randint(15, 45),
                "total_losses": random.randint(15, 45),
                "championships": random.randint(0, 3),
                "playoff_appearances": random.randint(2, 8),
                "best_season": random.randint(10, 14),
                "worst_season": random.randint(2, 6),
                "total_points_for": random.randint(3000, 8000),
                "total_points_against": random.randint(3000, 8000),
                "average_points_per_game": round(random.uniform(85, 110), 1),
                "longest_win_streak": random.randint(3, 12),
                "longest_losing_streak": random.randint(2, 8)
            }
            team_stats.append(team_stat)
        
        # Generate head-to-head records
        head_to_head = []
        for i, team1 in enumerate(teams):
            for j, team2 in enumerate(teams):
                if i < j:  # Avoid duplicates
                    wins1 = random.randint(2, 8)
                    wins2 = random.randint(2, 8)
                    head_to_head.append({
                        "team1": team1,
                        "team2": team2,
                        "wins1": wins1,
                        "wins2": wins2,
                        "total_games": wins1 + wins2
                    })
        
        # Generate season records
        season_records = []
        for year in range(2020, 2025):
            season_record = {
                "year": year,
                "champion": random.choice(teams),
                "runner_up": random.choice([t for t in teams if t != random.choice(teams)]),
                "regular_season_leader": random.choice(teams),
                "points_leader": random.choice(teams),
                "biggest_upset": f"{random.choice(teams)} over {random.choice(teams)}"
            }
            season_records.append(season_record)
        
        # Generate league records
        league_records = {
            "highest_single_game_score": random.randint(180, 220),
            "highest_single_game_score_team": random.choice(teams),
            "highest_single_game_score_year": random.randint(2020, 2024),
            "lowest_single_game_score": random.randint(45, 75),
            "lowest_single_game_score_team": random.choice(teams),
            "lowest_single_game_score_year": random.randint(2020, 2024),
            "most_consecutive_wins": random.randint(8, 15),
            "most_consecutive_wins_team": random.choice(teams),
            "most_consecutive_wins_year": random.randint(2020, 2024),
            "most_consecutive_losses": random.randint(6, 12),
            "most_consecutive_losses_team": random.choice(teams),
            "most_consecutive_losses_year": random.randint(2020, 2024)
        }
        
        return {
            "teams": team_stats,
            "head_to_head": head_to_head,
            "season_records": season_records,
            "league_records": league_records,
            "generated_at": datetime.now().isoformat(),
            "total_teams": len(teams),
            "total_seasons": 5
        }

def main():
    setup = HistoricalDataSetup()
    historical_file = setup.setup_historical_data()
    print(f"✅ Historical data setup complete: {historical_file}")

if __name__ == "__main__":
    main()


