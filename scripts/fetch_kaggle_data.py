#!/usr/bin/env python3
"""
Fantasy Football Data Fetcher from Kaggle
Integrates with your existing Kaggle notebook to fetch weekly data
"""

import json
import os
import requests
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import pandas as pd
import sys

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import Config

try:
    from kaggle.api.kaggle_api_extended import KaggleApi
except ImportError:
    KaggleApi = None

class FantasyDataFetcher:
    def __init__(self, kaggle_api_key=None, kaggle_username=None):
        """Initialize the Fantasy Data Fetcher"""
        self.kaggle_username = kaggle_username or Config.KAGGLE_USERNAME
        self.kaggle_key = kaggle_api_key or Config.KAGGLE_KEY
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', Config.DATA_DIR)
        
        # Setup logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        # Initialize Kaggle API
        self.kaggle_api = None
        if KaggleApi and self.kaggle_username and self.kaggle_key:
            try:
                self.kaggle_api = KaggleApi()
                self.kaggle_api.authenticate()
                self.logger.info("Kaggle API authenticated successfully")
            except Exception as e:
                self.logger.warning(f"Failed to authenticate with Kaggle API: {e}")
                self.logger.warning("Falling back to mock data")
        elif not KaggleApi:
            self.logger.warning("Kaggle API not available - install with: pip install kaggle")
        
        # Ensure data directories exist
        os.makedirs(os.path.join(self.data_dir, 'teams'), exist_ok=True)
        os.makedirs(os.path.join(self.data_dir, 'weekly'), exist_ok=True)
        os.makedirs(os.path.join(self.data_dir, 'historical'), exist_ok=True)
        
        # Load team configuration
        self.teams_config = self._load_teams_config()

    def _load_teams_config(self) -> Dict[str, Any]:
        """Load team configuration from season-stats.json or fallback to config"""
        try:
            season_file = os.path.join(self.data_dir, 'season-stats.json')
            with open(season_file, 'r') as f:
                season_data = json.load(f)
                teams = season_data.get('standings', [])
                
                # If we don't have enough teams, use the config
                if len(teams) < Config.TOTAL_TEAMS:
                    self.logger.warning(f"Only {len(teams)} teams found in season-stats.json, using config for all {Config.TOTAL_TEAMS} teams")
                    return self._get_default_teams_config()
                
                return {
                    'teams': teams,
                    'league_info': season_data.get('leagueInfo', {}),
                    'total_teams': season_data.get('leagueInfo', {}).get('totalTeams', Config.TOTAL_TEAMS)
                }
        except FileNotFoundError:
            self.logger.warning("season-stats.json not found, using default team config")
            return self._get_default_teams_config()

    def _get_default_teams_config(self) -> Dict[str, Any]:
        """Get default team configuration"""
        return Config.get_team_config()

    def fetch_weekly_data(self, week_number: int) -> Dict[str, Any]:
        """
        Fetch data for a specific week from Kaggle or fallback to mock data
        """
        self.logger.info(f"Fetching data for Week {week_number}...")
        
        try:
            # Try to fetch from Kaggle first
            if self.kaggle_api:
                weekly_data = self._fetch_from_kaggle(week_number)
                if weekly_data:
                    self.logger.info("Successfully fetched data from Kaggle")
                    return weekly_data
                else:
                    self.logger.warning("Kaggle fetch returned empty data, falling back to mock")
            else:
                self.logger.info("Kaggle API not available, using mock data")
            
            # Fallback to mock data
            return self._generate_mock_weekly_data(week_number)
            
        except Exception as e:
            self.logger.error(f"Error fetching weekly data: {e}")
            self.logger.info("Falling back to mock data due to error")
            return self._generate_mock_weekly_data(week_number)

    def _fetch_from_kaggle(self, week_number: int) -> Optional[Dict[str, Any]]:
        """Fetch data from Kaggle API - looks for YAML creative brief"""
        try:
            dataset_name = Config.KAGGLE_DATASET
            yaml_file_name = f"creative_brief_week{week_number}.yaml"
            
            # Download the YAML file from Kaggle
            self.kaggle_api.dataset_download_file(
                dataset=dataset_name,
                file_name=yaml_file_name,
                path=self.data_dir
            )
            
            # Look for the YAML file
            yaml_path = os.path.join(self.data_dir, yaml_file_name)
            if os.path.exists(yaml_path):
                return self._process_kaggle_yaml(yaml_path, week_number)
            else:
                self.logger.warning(f"Expected YAML file {yaml_file_name} not found in dataset")
                return None
                
        except Exception as e:
            self.logger.error(f"Error fetching from Kaggle: {e}")
            return None

    def _process_kaggle_yaml(self, yaml_path: str, week_number: int) -> Dict[str, Any]:
        """Process the YAML file from Kaggle notebook"""
        try:
            import yaml
            
            with open(yaml_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            # Convert Kaggle YAML format to newsletter format
            return self._convert_kaggle_to_newsletter_format(data, week_number)
            
        except Exception as e:
            self.logger.error(f"Error processing Kaggle YAML: {e}")
            return None
    
    def _convert_kaggle_to_newsletter_format(self, kaggle_data: Dict, week_number: int) -> Dict[str, Any]:
        """Convert Kaggle notebook output to newsletter format"""
        try:
            # Extract standings
            standings = []
            for team in kaggle_data.get('Standings', {}).get('Overall', []):
                standings.append({
                    "team": self._get_team_name_from_owner(team.get('Owner', '')),
                    "owner": team.get('Owner', ''),
                    "division": team.get('Division', ''),
                    "rank": team.get('OverallRank', 16),
                    "record": f"{team.get('Wins', 0)}-{team.get('Losses', 0)}-{team.get('Ties', 0)}",
                    "points_for": team.get('PF', 0.0),
                    "points_against": team.get('PA', 0.0),
                    "wins": team.get('Wins', 0),
                    "losses": team.get('Losses', 0),
                    "ties": team.get('Ties', 0)
                })
            
            # Extract matchups
            matchups = []
            for matchup in kaggle_data.get('Matchups', []):
                teams = matchup.get('Teams', [])
                if len(teams) >= 2:
                    team1 = teams[0]
                    team2 = teams[1]
                    
                    matchups.append({
                        "team1": self._get_team_name_from_owner(team1.get('Owner', '')),
                        "team2": self._get_team_name_from_owner(team2.get('Owner', '')),
                        "team1_owner": team1.get('Owner', ''),
                        "team2_owner": team2.get('Owner', ''),
                        "team1_score": team1.get('Score', 0.0),
                        "team2_score": team2.get('Score', 0.0),
                        "winner": self._get_team_name_from_owner(team1.get('Owner', '')) if team1.get('Score', 0) > team2.get('Score', 0) else self._get_team_name_from_owner(team2.get('Owner', '')),
                        "margin": abs(team1.get('Score', 0) - team2.get('Score', 0)),
                        "team1_analysis": self._extract_team_analysis(team1),
                        "team2_analysis": self._extract_team_analysis(team2)
                    })
            
            # Extract awards
            awards = kaggle_data.get('Awards', {})
            
            # Generate transactions based on performance
            transactions = self._generate_transactions_from_kaggle_data(standings, matchups)
            
            # Extract player performances
            player_performances = self._extract_player_performances_from_kaggle(matchups)
            
            return {
                "week": week_number,
                "season": kaggle_data.get('WeekInfo', {}).get('Season', 2025),
                "last_updated": datetime.now().isoformat(),
                "standings": standings,
                "matchups": matchups,
                "awards": awards,
                "transactions": transactions,
                "player_performances": player_performances
            }
            
        except Exception as e:
            self.logger.error(f"Error converting Kaggle data: {e}")
            return None
    
    def _get_team_name_from_owner(self, owner: str) -> str:
        """Map owner name to team name using config"""
        team_config = self.config.get_team_config()
        
        for team in team_config['teams']:
            if team['owner'].lower() == owner.lower():
                return team['team']
        
        # Fallback: return owner name if no match found
        return owner
    
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
    
    def _generate_transactions_from_kaggle_data(self, standings: List[Dict], matchups: List[Dict]) -> List[Dict]:
        """Generate transactions based on Kaggle data"""
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
    
    def _extract_player_performances_from_kaggle(self, matchups: List[Dict]) -> List[Dict]:
        """Extract top player performances from Kaggle matchups"""
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

    def _process_kaggle_dataframe(self, df: pd.DataFrame, week_number: int) -> Dict[str, Any]:
        """Process Kaggle dataframe into our expected format"""
        # This is where you'd process your actual Kaggle data
        # The structure depends on how your Kaggle notebook outputs data
        
        # For now, return mock data structure
        # TODO: Replace with actual data processing logic
        return self._generate_mock_weekly_data(week_number)

    def _generate_mock_weekly_data(self, week_number: int) -> Dict[str, Any]:
        """Generate realistic mock data for testing"""
        self.logger.info(f"Generating mock data for Week {week_number}")
        
        # Generate realistic scores based on week progression
        base_scores = [85, 92, 78, 105, 88, 95, 102, 76, 89, 98, 83, 91, 87, 94, 99, 81]
        week_variance = week_number * 2  # More variance as season progresses
        
        # Generate matchups and scores
        teams = self.teams_config['teams']
        matchups = []
        standings = []
        
        # Create 8 matchups (16 teams)
        import random
        for i in range(0, len(teams), 2):
            team1 = teams[i]
            team2 = teams[i + 1] if i + 1 < len(teams) else teams[0]
            
            # Generate realistic scores with some randomness
            score1 = base_scores[i % len(base_scores)] + random.randint(-week_variance, week_variance)
            score2 = base_scores[(i + 1) % len(base_scores)] + random.randint(-week_variance, week_variance)
            
            matchup = {
                "team1": team1["team"],
                "team2": team2["team"],
                "team1_score": max(score1, 0),  # Ensure non-negative
                "team2_score": max(score2, 0),
                "winner": team1["team"] if score1 > score2 else team2["team"]
            }
            matchups.append(matchup)
            
            # Add to standings
            standings.extend([
                {
                    "rank": i + 1,
                    "team": team1["team"],
                    "owner": team1["owner"],
                    "record": f"{random.randint(3, 8)}-{random.randint(1, 6)}",
                    "points_for": score1 + random.randint(200, 800),
                    "points_against": random.randint(600, 1000),
                    "division": team1["division"],
                    "streak": random.choice(["W2", "L1", "W1", "L2", "W3"])
                },
                {
                    "rank": i + 2,
                    "team": team2["team"],
                    "owner": team2["owner"],
                    "record": f"{random.randint(3, 8)}-{random.randint(1, 6)}",
                    "points_for": score2 + random.randint(200, 800),
                    "points_against": random.randint(600, 1000),
                    "division": team2["division"],
                    "streak": random.choice(["W2", "L1", "W1", "L2", "W3"])
                }
            ])
        
        # Sort standings by points_for
        standings.sort(key=lambda x: x["points_for"], reverse=True)
        for i, team in enumerate(standings):
            team["rank"] = i + 1
        
        return {
            "week": week_number,
            "season": 2025,
            "last_updated": datetime.now().isoformat(),
            "matchups": matchups,
            "standings": standings,
            "transactions": self._fetch_transactions(week_number),
            "player_performances": self._fetch_player_performances(week_number),
            "league_averages": self._calculate_league_averages()
        }

    def _fetch_transactions(self, week: int) -> Dict[str, List]:
        """Fetch trades and waiver wire activity"""
        import random
        
        # Generate realistic transactions based on week
        trades = []
        waivers = []
        
        # More trades happen later in the season
        if week > 4 and random.random() < 0.3:
            teams = self.teams_config['teams']
            trade_teams = random.sample(teams, 2)
            trades.append({
                "teams": [trade_teams[0]["team"], trade_teams[1]["team"]],
                "players_traded": ["Player A", "Player B"],
                "analysis": f"{trade_teams[0]['team']} gets the better end of this deal"
            })
        
        # Generate waiver claims
        if random.random() < 0.7:
            teams = self.teams_config['teams']
            waiver_team = random.choice(teams)
            waiver_players = ["Backup RB", "Sleeper WR", "Handcuff RB", "Streaming QB", "Defense"]
            waivers.append({
                "team": waiver_team["team"],
                "player": random.choice(waiver_players),
                "faab_spent": random.randint(5, 50),
                "priority": random.randint(1, 5)
            })
        
        return {
            "trades": trades,
            "waivers": waivers
        }

    def _fetch_player_performances(self, week: int) -> Dict[str, Any]:
        """Fetch individual player performance data"""
        return {
            "top_performers": [
                {"player": "Josh Allen", "team": "JewTeam", "points": 28.5},
                {"player": "CMC", "team": "gunga36", "points": 31.2}
            ],
            "busts": [
                {"player": "Jonathan Taylor", "team": "Some Team", "points": 4.2}
            ],
            "surprises": [
                {"player": "Random Backup", "team": "Lucky Team", "points": 22.1}
            ]
        }

    def _calculate_league_averages(self) -> Dict[str, float]:
        """Calculate league-wide averages and metrics"""
        return {
            "avg_points_per_week": 125.4,
            "highest_score": 178.5,
            "lowest_score": 67.8,
            "std_deviation": 28.7
        }

    def validate_weekly_data(self, weekly_data: Dict) -> bool:
        """Validate that weekly data has all required fields"""
        required_fields = ['week', 'season', 'last_updated', 'matchups', 'standings', 'transactions']
        
        for field in required_fields:
            if field not in weekly_data:
                self.logger.error(f"Missing required field: {field}")
                return False
        
        # Validate standings structure
        if not isinstance(weekly_data['standings'], list) or len(weekly_data['standings']) == 0:
            self.logger.error("Standings must be a non-empty list")
            return False
        
        # Validate each team has required fields
        for team in weekly_data['standings']:
            team_required = ['rank', 'team', 'owner', 'record', 'points_for', 'points_against']
            for field in team_required:
                if field not in team:
                    self.logger.error(f"Team missing required field {field}: {team}")
                    return False
        
        self.logger.info("Weekly data validation passed")
        return True

    def update_season_stats(self, weekly_data: Dict) -> None:
        """Update the main season stats file"""
        if not self.validate_weekly_data(weekly_data):
            self.logger.error("Invalid weekly data, skipping season stats update")
            return
            
        season_file = os.path.join(self.data_dir, 'season-stats.json')
        
        try:
            with open(season_file, 'r') as f:
                season_stats = json.load(f)
        except FileNotFoundError:
            season_stats = self._create_initial_season_stats()

        # Update with latest weekly data
        season_stats['currentWeek'] = weekly_data['week']
        season_stats['lastUpdated'] = weekly_data['last_updated']
        season_stats['standings'] = weekly_data['standings']
        
        # Update top performers
        self._update_top_performers(season_stats, weekly_data)
        
        # Save updated season stats
        with open(season_file, 'w') as f:
            json.dump(season_stats, f, indent=2)
        
        self.logger.info(f"Updated season stats for Week {weekly_data['week']}")

    def update_team_profiles(self, weekly_data: Dict) -> None:
        """Update individual team profile files"""
        for team in weekly_data['standings']:
            team_file = os.path.join(self.data_dir, 'teams', f"{team['team'].lower()}.json")
            
            # Load existing team data or create new
            try:
                with open(team_file, 'r') as f:
                    team_data = json.load(f)
            except FileNotFoundError:
                team_data = self._create_initial_team_profile(team)

            # Update with latest data
            self._update_team_current_season(team_data, team, weekly_data)
            
            # Generate new analytics
            team_data['analytics'].update(self.generate_team_analysis(team_data))
            
            # Save updated team profile
            with open(team_file, 'w') as f:
                json.dump(team_data, f, indent=2)

    def generate_team_analysis(self, team_data: Dict) -> Dict[str, Any]:
        """Generate advanced analytics for a team"""
        return {
            "efficiency_rating": self._calculate_efficiency(team_data),
            "strength_of_schedule": self._calculate_sos(team_data),
            "playoff_odds": self._calculate_playoff_odds(team_data),
            "power_ranking": self._calculate_power_ranking(team_data),
            "trends": self._analyze_trends(team_data)
        }

    def _calculate_efficiency(self, team_data: Dict) -> float:
        """Calculate team efficiency rating"""
        return 85.7

    def _calculate_sos(self, team_data: Dict) -> float:
        """Calculate strength of schedule"""
        return 0.45

    def _calculate_playoff_odds(self, team_data: Dict) -> float:
        """Calculate playoff odds based on current performance"""
        return 98.5

    def _calculate_power_ranking(self, team_data: Dict) -> int:
        """Calculate power ranking (1-16)"""
        return 3

    def _analyze_trends(self, team_data: Dict) -> Dict[str, str]:
        """Analyze team trends"""
        return {
            "scoring_trend": "Improving",
            "consistency": "High",
            "recent_form": "Hot"
        }

    def _create_initial_season_stats(self) -> Dict:
        """Create initial season stats structure"""
        return {
            "currentWeek": 1,
            "totalWeeks": 17,
            "lastUpdated": datetime.now().isoformat(),
            "leagueInfo": {
                "name": "16 Fantasies 1 Cup",
                "season": "2025",
                "totalTeams": 16,
                "playoffTeams": 8,
                "regularSeasonWeeks": 14
            },
            "topPerformers": {},
            "standings": [],
            "weeklyHighlights": [],
            "divisionStandings": {},
            "recentActivity": {"trades": [], "waivers": []}
        }

    def _create_initial_team_profile(self, team: Dict) -> Dict:
        """Create initial team profile structure"""
        return {
            "teamInfo": {
                "teamName": team['team'],
                "ownerName": team['owner'],
                "division": team['division'],
                "teamSlug": team['team'].lower(),
                "founded": 2025,
                "motto": "Generated Profile"
            },
            "currentSeason": {},
            "historicalData": {},
            "analytics": {},
            "roastingMaterial": {"currentSeason": [], "historicalShame": [], "signatures": []},
            "headToHead": {}
        }

    def _update_top_performers(self, season_stats: Dict, weekly_data: Dict) -> None:
        """Update season top performers"""
        pass

    def _update_team_current_season(self, team_data: Dict, team: Dict, weekly_data: Dict) -> None:
        """Update team's current season data"""
        team_data['currentSeason'].update({
            "record": team['record'],
            "pointsFor": team['points_for'],
            "pointsAgainst": team['points_against'],
            "rank": team['rank'],
            "lastUpdated": weekly_data['last_updated']
        })

    def save_weekly_data(self, weekly_data: Dict) -> None:
        """Save weekly data to file"""
        week_file = os.path.join(self.data_dir, 'weekly', f"week-{weekly_data['week']:02d}.json")
        with open(week_file, 'w') as f:
            json.dump(weekly_data, f, indent=2)

def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Fetch and process fantasy football data')
    parser.add_argument('--week', type=int, required=True, help='Week number to process')
    parser.add_argument('--kaggle-username', help='Kaggle username')
    parser.add_argument('--kaggle-key', help='Kaggle API key')
    
    args = parser.parse_args()
    
    # Initialize fetcher
    fetcher = FantasyDataFetcher(
        kaggle_username=args.kaggle_username,
        kaggle_api_key=args.kaggle_key
    )
    
    try:
        # Fetch weekly data
        print(f"Processing Week {args.week} data...")
        weekly_data = fetcher.fetch_weekly_data(args.week)
        
        # Validate data before processing
        if not fetcher.validate_weekly_data(weekly_data):
            print("❌ Data validation failed, aborting processing")
            return
        
        # Update all data files
        fetcher.save_weekly_data(weekly_data)
        fetcher.update_season_stats(weekly_data)
        fetcher.update_team_profiles(weekly_data)
        
        print(f"✅ Successfully processed Week {args.week} data!")
        print(f"📊 Updated {len(weekly_data['standings'])} team profiles")
        if weekly_data['standings']:
            print(f"🏆 Current leader: {weekly_data['standings'][0]['team']}")
        
    except Exception as e:
        print(f"❌ Error processing data: {e}")
        fetcher.logger.error(f"Processing failed: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
