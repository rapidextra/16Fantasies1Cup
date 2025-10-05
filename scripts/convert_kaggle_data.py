#!/usr/bin/env python3
"""
Kaggle Data Converter
Converts YAML data from Kaggle script into newsletter-compatible JSON format
"""

import yaml
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import Config

class KaggleDataConverter:
    def __init__(self):
        self.config = Config()
        
    def convert_yaml_to_newsletter_format(self, yaml_file_path: str, week_number: int) -> Dict:
        """Convert Kaggle YAML data to newsletter JSON format"""
        print(f"Converting Kaggle data for Week {week_number}...")
        
        # Load YAML data
        with open(yaml_file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        # Convert standings
        standings = self._convert_standings(data.get('Standings', {}).get('Overall', []))
        
        # Convert matchups
        matchups = self._convert_matchups(data.get('Matchups', []))
        
        # Convert awards
        awards = self._convert_awards(data.get('Awards', {}))
        
        # Create weekly data structure
        weekly_data = {
            "week": week_number,
            "season": data.get('WeekInfo', {}).get('Season', 2025),
            "last_updated": datetime.now().isoformat(),
            "standings": standings,
            "matchups": matchups,
            "awards": awards,
            "transactions": self._generate_transactions_from_data(standings, matchups),
            "player_performances": self._extract_player_performances(matchups)
        }
        
        return weekly_data
    
    def _convert_standings(self, overall_standings: List[Dict]) -> List[Dict]:
        """Convert overall standings to newsletter format"""
        standings = []
        
        for team in overall_standings:
            # Map owner names to team names using config
            owner = team.get('Owner', '')
            team_name = self._get_team_name_from_owner(owner)
            
            standings.append({
                "team": team_name,
                "owner": owner,
                "division": team.get('Division', ''),
                "rank": team.get('OverallRank', 16),
                "record": f"{team.get('Wins', 0)}-{team.get('Losses', 0)}-{team.get('Ties', 0)}",
                "points_for": team.get('PF', 0.0),
                "points_against": team.get('PA', 0.0),
                "wins": team.get('Wins', 0),
                "losses": team.get('Losses', 0),
                "ties": team.get('Ties', 0)
            })
        
        return standings
    
    def _convert_matchups(self, matchups_data: List[Dict]) -> List[Dict]:
        """Convert matchups to newsletter format"""
        matchups = []
        
        for matchup in matchups_data:
            teams = matchup.get('Teams', [])
            if len(teams) >= 2:
                team1 = teams[0]
                team2 = teams[1]
                
                # Get team names from owners
                team1_name = self._get_team_name_from_owner(team1.get('Owner', ''))
                team2_name = self._get_team_name_from_owner(team2.get('Owner', ''))
                
                matchup_data = {
                    "team1": team1_name,
                    "team2": team2_name,
                    "team1_owner": team1.get('Owner', ''),
                    "team2_owner": team2.get('Owner', ''),
                    "team1_score": team1.get('Score', 0.0),
                    "team2_score": team2.get('Score', 0.0),
                    "winner": team1_name if team1.get('Score', 0) > team2.get('Score', 0) else team2_name,
                    "margin": abs(team1.get('Score', 0) - team2.get('Score', 0)),
                    "team1_analysis": self._extract_team_analysis(team1),
                    "team2_analysis": self._extract_team_analysis(team2)
                }
                
                matchups.append(matchup_data)
        
        return matchups
    
    def _extract_team_analysis(self, team_data: Dict) -> Dict:
        """Extract team analysis from matchup data"""
        return {
            "mvp": team_data.get('MVP', {}).get('Player', 'Unknown') if team_data.get('MVP') else 'Unknown',
            "bust": team_data.get('Bust', {}).get('Player', 'Unknown') if team_data.get('Bust') else 'Unknown',
            "coach_rating": team_data.get('CoachRating', 0.0),
            "luck_rating": team_data.get('LuckRating', 0.0),
            "key_mistake": team_data.get('KeyMistake', 'No obvious mistake'),
            "optimal_score": team_data.get('OptimalScore', 0.0),
            "ugly": team_data.get('Ugly', 0.0)
        }
    
    def _convert_awards(self, awards_data: Dict) -> Dict:
        """Convert awards to newsletter format"""
        awards = {}
        
        if 'HighestScorer' in awards_data:
            highest = awards_data['HighestScorer']
            awards['highest_scorer'] = {
                "team": self._get_team_name_from_owner(highest.get('Owner', '')),
                "owner": highest.get('Owner', ''),
                "score": highest.get('Score', 0.0)
            }
        
        if 'CoachOfTheWeek' in awards_data:
            coach = awards_data['CoachOfTheWeek']
            awards['coach_of_week'] = {
                "team": self._get_team_name_from_owner(coach.get('Owner', '')),
                "owner": coach.get('Owner', ''),
                "rating": coach.get('CoachRating', 0.0)
            }
        
        if 'BoneheadOfTheWeek' in awards_data:
            bonehead = awards_data['BoneheadOfTheWeek']
            awards['bonehead_of_week'] = {
                "team": self._get_team_name_from_owner(bonehead.get('Owner', '')),
                "owner": bonehead.get('Owner', ''),
                "mistake": bonehead.get('KeyMistake', ''),
                "bench_points_lost": bonehead.get('BenchPointsLost', 0.0),
                "loss_margin": bonehead.get('LossMargin', 0.0)
            }
        
        if 'Luckiest' in awards_data:
            lucky = awards_data['Luckiest']
            awards['luckiest'] = {
                "team": self._get_team_name_from_owner(lucky.get('Owner', '')),
                "owner": lucky.get('Owner', ''),
                "score": lucky.get('Score', 0.0),
                "description": lucky.get('Description', '')
            }
        
        if 'Unluckiest' in awards_data:
            unlucky = awards_data['Unluckiest']
            awards['unluckiest'] = {
                "team": self._get_team_name_from_owner(unlucky.get('Owner', '')),
                "owner": unlucky.get('Owner', ''),
                "score": unlucky.get('Score', 0.0),
                "description": unlucky.get('Description', '')
            }
        
        return awards
    
    def _get_team_name_from_owner(self, owner: str) -> str:
        """Map owner name to team name using config"""
        team_config = self.config.get_team_config()
        
        for team in team_config['teams']:
            if team['owner'].lower() == owner.lower():
                return team['team']
        
        # Fallback: return owner name if no match found
        return owner
    
    def _generate_transactions_from_data(self, standings: List[Dict], matchups: List[Dict]) -> List[Dict]:
        """Generate mock transactions based on the data"""
        transactions = []
        
        # Generate some mock transactions based on performance
        for team in standings[:5]:  # Top 5 teams
            if team['points_for'] > 200:  # High scoring teams
                transactions.append({
                    "type": "trade",
                    "team": team['team'],
                    "owner": team['owner'],
                    "description": f"{team['owner']} made a strategic trade to strengthen their lineup",
                    "impact": "positive"
                })
        
        return transactions
    
    def _extract_player_performances(self, matchups: List[Dict]) -> List[Dict]:
        """Extract top player performances from matchups"""
        performances = []
        
        for matchup in matchups:
            # Add team performances
            performances.append({
                "player": f"{matchup['team1_owner']} (Team)",
                "position": "TM",
                "points": matchup['team1_score'],
                "team": matchup['team1']
            })
            performances.append({
                "player": f"{matchup['team2_owner']} (Team)",
                "position": "TM", 
                "points": matchup['team2_score'],
                "team": matchup['team2']
            })
        
        # Sort by points and return top 10
        performances.sort(key=lambda x: x['points'], reverse=True)
        return performances[:10]
    
    def save_weekly_data(self, weekly_data: Dict, week_number: int) -> str:
        """Save converted data to weekly JSON file"""
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'weekly')
        os.makedirs(data_dir, exist_ok=True)
        
        filename = f"week-{week_number:02d}.json"
        filepath = os.path.join(data_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(weekly_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Converted data saved to {filepath}")
        return filepath

def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Convert Kaggle YAML data to newsletter format')
    parser.add_argument('--yaml-file', required=True, help='Path to YAML file from Kaggle')
    parser.add_argument('--week', type=int, required=True, help='Week number')
    
    args = parser.parse_args()
    
    # Initialize converter
    converter = KaggleDataConverter()
    
    try:
        # Convert data
        weekly_data = converter.convert_yaml_to_newsletter_format(args.yaml_file, args.week)
        
        # Save data
        filepath = converter.save_weekly_data(weekly_data, args.week)
        
        print(f"✅ Successfully converted Week {args.week} data!")
        print(f"📁 Saved to: {filepath}")
        
    except Exception as e:
        print(f"❌ Error converting data: {e}")
        raise

if __name__ == "__main__":
    main()

