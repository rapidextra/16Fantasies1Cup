#!/usr/bin/env python3
"""
Pre-Week Fantasy Football Newsletter Generator
Creates HTML preview newsletters with predictions, matchups, and analysis
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
from jinja2 import Template
import sys
import random

# Add parent directory to path to import roasting engine
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from scripts.roasting_engine import RoastingEngine
from config import Config

class PreWeekNewsletterGenerator:
    def __init__(self):
        self.project_root = os.path.dirname(os.path.dirname(__file__))
        self.data_dir = os.path.join(self.project_root, 'data')
        self.template_file = os.path.join(self.project_root, 'preweek-template.html')
        self.roasting_engine = RoastingEngine()
        self.config = Config()
        
    def generate_preweek_newsletter(self, week_number: int, week_title: str = None) -> str:
        """Generate a complete pre-week newsletter for the given week"""
        print(f"Generating pre-week newsletter for Week {week_number}...")
        
        # Load data
        weekly_data = self._load_weekly_data(week_number)
        season_data = self._load_season_data()
        
        # Generate title if not provided
        if not week_title:
            week_title = self._generate_preweek_title(week_number)
        
        # Load template
        with open(self.template_file, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Generate newsletter content
        newsletter_html = self._populate_template(
            template_content,
            week_number,
            week_title,
            weekly_data,
            season_data
        )
        
        # Save newsletter
        output_file = f"preweek-{week_number:02d}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(newsletter_html)
        
        print(f"✅ Pre-week newsletter saved as {output_file}")
        print(f"📰 Pre-week newsletter generated successfully!")
        print(f"📁 Saved to: {os.path.abspath(output_file)}")
        
        return output_file
    
    def _load_weekly_data(self, week_number: int) -> Dict:
        """Load weekly data for predictions"""
        try:
            week_file = os.path.join(self.data_dir, 'weekly', f'week-{week_number:02d}.json')
            with open(week_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Try to load the most recent available data for standings
            latest_week = self._find_latest_weekly_data()
            if latest_week:
                print(f"Using Week {latest_week} data for standings preview")
                return self._load_weekly_data(latest_week)
            else:
                # Generate mock data for predictions
                return self._generate_mock_weekly_data(week_number)
    
    def _find_latest_weekly_data(self) -> int:
        """Find the latest available weekly data"""
        import glob
        weekly_files = glob.glob(os.path.join(self.data_dir, 'weekly', 'week-*.json'))
        if not weekly_files:
            return None
        
        # Extract week numbers and find the highest
        week_numbers = []
        for file_path in weekly_files:
            filename = os.path.basename(file_path)
            try:
                week_num = int(filename.replace('week-', '').replace('.json', ''))
                week_numbers.append(week_num)
            except ValueError:
                continue
        
        return max(week_numbers) if week_numbers else None
    
    def _load_season_data(self) -> Dict:
        """Load season data"""
        try:
            season_file = os.path.join(self.data_dir, 'season-stats.json')
            with open(season_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._create_initial_season_stats()
    
    def _generate_mock_weekly_data(self, week_number: int) -> Dict:
        """Generate mock data for pre-week predictions"""
        teams = self.config.get_team_config()['teams']
        
        # Generate predicted matchups
        matchups = []
        for i in range(0, len(teams), 2):
            team1 = teams[i]
            team2 = teams[i + 1] if i + 1 < len(teams) else teams[0]
            
            # Generate predicted scores with some randomness
            base_score1 = random.randint(80, 140)
            base_score2 = random.randint(80, 140)
            
            matchup = {
                "team1": team1["team"],
                "team2": team2["team"],
                "team1_owner": team1["owner"],
                "team2_owner": team2["owner"],
                "team1_predicted_score": base_score1,
                "team2_predicted_score": base_score2,
                "predicted_winner": team1["team"] if base_score1 > base_score2 else team2["team"],
                "confidence": random.choice(["High", "Medium", "Low"]),
                "key_matchup": random.choice([True, False])
            }
            matchups.append(matchup)
        
        return {
            "week": week_number,
            "season": 2025,
            "last_updated": datetime.now().isoformat(),
            "matchups": matchups,
            "predictions": self._generate_predictions(teams, matchups),
            "storylines": self._generate_storylines(teams, matchups),
            "waiver_wire": self._generate_waiver_wire_picks(),
            "weather_watch": self._generate_weather_watch(),
            "injury_report": self._generate_injury_report()
        }
    
    def _generate_predictions(self, teams: List[Dict], matchups: List[Dict]) -> Dict[str, Any]:
        """Generate predictions for the week"""
        return {
            "upset_alert": random.choice(matchups),
            "blowout_of_the_week": max(matchups, key=lambda x: abs(x['team1_predicted_score'] - x['team2_predicted_score'])),
            "closest_matchup": min(matchups, key=lambda x: abs(x['team1_predicted_score'] - x['team2_predicted_score'])),
            "highest_scorer": max(teams, key=lambda x: random.randint(100, 180)),
            "sleeper_pick": random.choice(teams)
        }
    
    def _generate_storylines(self, teams: List[Dict], matchups: List[Dict]) -> List[str]:
        """Generate storylines for the week"""
        storylines = [
            f"Can {random.choice(teams)['team']} break their {random.randint(2, 5)}-game losing streak?",
            f"The battle for playoff positioning heats up as {random.choice(teams)['team']} faces {random.choice(teams)['team']}",
            f"Will {random.choice(teams)['team']} finally live up to their preseason hype?",
            f"Rivalry week continues as {random.choice(teams)['team']} looks to get revenge on {random.choice(teams)['team']}",
            f"Can {random.choice(teams)['team']} maintain their perfect record against {random.choice(teams)['team']}?",
            f"The {random.choice(teams)['division']} division title race comes down to this week",
            f"Will {random.choice(teams)['team']} be the first team eliminated from playoff contention?",
            f"The waiver wire hero {random.choice(teams)['team']} picked up last week could be the difference maker"
        ]
        
        return random.sample(storylines, 4)
    
    def _generate_waiver_wire_picks(self) -> List[Dict[str, Any]]:
        """Generate waiver wire recommendations"""
        positions = ["QB", "RB", "WR", "TE", "K", "DEF"]
        players = [
            "Sleeper RB", "Backup QB", "Handcuff RB", "Streaming TE", 
            "Hot WR", "Rookie RB", "Veteran WR", "Kicker Stream"
        ]
        
        picks = []
        for _ in range(5):
            picks.append({
                "player": random.choice(players),
                "position": random.choice(positions),
                "team": random.choice(["FA", "Waivers"]),
                "reason": random.choice([
                    "Favorable matchup this week",
                    "Injury to starter opens opportunity",
                    "Weather conditions favor this position",
                    "Revenge game narrative",
                    "Prime time performance incoming"
                ]),
                "faab_suggestion": random.randint(5, 50)
            })
        
        return picks
    
    def _generate_weather_watch(self) -> List[Dict[str, Any]]:
        """Generate weather impact analysis"""
        cities = ["Buffalo", "Green Bay", "Chicago", "Denver", "Cleveland", "Pittsburgh"]
        conditions = ["Snow", "Rain", "Wind", "Cold", "Heat", "Clear"]
        
        weather_impacts = []
        for _ in range(3):
            city = random.choice(cities)
            condition = random.choice(conditions)
            weather_impacts.append({
                "city": city,
                "condition": condition,
                "impact": self._get_weather_impact(condition),
                "games_affected": random.randint(1, 3)
            })
        
        return weather_impacts
    
    def _get_weather_impact(self, condition: str) -> str:
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
    
    def _generate_injury_report(self) -> List[Dict[str, Any]]:
        """Generate injury report"""
        injuries = [
            {"player": "Star RB", "status": "Questionable", "impact": "High"},
            {"player": "Starting QB", "status": "Probable", "impact": "Medium"},
            {"player": "WR1", "status": "Doubtful", "impact": "High"},
            {"player": "Defense", "status": "Out", "impact": "Medium"},
            {"player": "Kicker", "status": "Questionable", "impact": "Low"}
        ]
        
        return random.sample(injuries, 3)
    
    def _generate_preweek_title(self, week_number: int) -> str:
        """Generate a pre-week title"""
        titles = [
            "The Calm Before the Storm",
            "Prediction Time",
            "Crystal Ball Gazing",
            "The Preview Show",
            "Week of Reckoning",
            "The Setup",
            "Pre-Game Hype",
            "The Anticipation",
            "Week of Destiny",
            "The Countdown Begins"
        ]
        
        return random.choice(titles)
    
    def _populate_template(self, template_content: str, week_number: int, week_title: str, 
                          weekly_data: Dict, season_data: Dict) -> str:
        """Populate the template with data"""
        
        # Generate sections
        standings_section = self._generate_standings_preview(weekly_data, season_data)
        matchups_section = self._generate_matchups_preview(weekly_data)
        predictions_section = self._generate_predictions_section(weekly_data)
        storylines_section = self._generate_storylines_section(weekly_data)
        waiver_section = self._generate_waiver_section(weekly_data)
        weather_section = self._generate_weather_section(weekly_data)
        injury_section = self._generate_injury_section(weekly_data)
        roasting_section = self._generate_preweek_roasts(weekly_data)
        
        # Replace template placeholders
        template = Template(template_content)
        return template.render(
            week_number=week_number,
            week_title=week_title,
            current_date=datetime.now().strftime("%B %d, %Y"),
            standings_section=standings_section,
            matchups_section=matchups_section,
            predictions_section=predictions_section,
            storylines_section=storylines_section,
            waiver_section=waiver_section,
            weather_section=weather_section,
            injury_section=injury_section,
            roasting_section=roasting_section
        )
    
    def _generate_standings_preview(self, weekly_data: Dict, season_data: Dict) -> str:
        """Generate standings preview section"""
        standings = weekly_data.get('standings', [])
        
        if not standings:
            return "<p>No standings data available for preview.</p>"
        
        html = '''
        <section class="card px-5 sm:px-6 py-6">
          <h2 class="font-header text-3xl sm:text-4xl font-bold text-center mb-6">📊 Current Standings</h2>
          <div class="grid grid-cols-1 gap-4 lg:grid-cols-2">
        '''
        
        # Top 8 teams
        for i, team in enumerate(standings[:8]):
            html += f'''
            <div class="sub-card p-4">
              <div class="flex justify-between items-center">
                <div>
                  <p class="font-bold">{i+1}. {team.get('team', 'Unknown')}</p>
                  <p class="text-sm text-slate-400">{team.get('owner', 'Unknown')} • {team.get('record', '0-0')}</p>
                </div>
                <div class="text-right">
                  <p class="text-sm">PF: {team.get('points_for', 0):.1f}</p>
                  <p class="text-xs text-slate-400">PA: {team.get('points_against', 0):.1f}</p>
                </div>
              </div>
            </div>
            '''
        
        html += '</div></section>'
        return html
    
    def _generate_matchups_preview(self, weekly_data: Dict) -> str:
        """Generate matchups preview section"""
        matchups = weekly_data.get('matchups', [])
        
        html = '''
        <section class="card px-5 sm:px-6 py-6">
          <h2 class="font-header text-3xl sm:text-4xl font-bold text-center mb-6">⚔️ Week Matchups</h2>
          <div class="grid grid-cols-1 gap-4 lg:grid-cols-2">
        '''
        
        for matchup in matchups:
            confidence_color = {
                "High": "text-green-400",
                "Medium": "text-yellow-400", 
                "Low": "text-red-400"
            }.get(matchup.get('confidence', 'Medium'), 'text-yellow-400')
            
            html += f'''
            <div class="sub-card p-4">
              <div class="text-center mb-3">
                <p class="font-bold text-lg">{matchup.get('team1', 'Team 1')} vs {matchup.get('team2', 'Team 2')}</p>
                <p class="text-sm text-slate-400">{matchup.get('team1_owner', '')} vs {matchup.get('team2_owner', '')}</p>
              </div>
              <div class="flex justify-between items-center">
                <div class="text-center">
                  <p class="text-2xl font-bold">{matchup.get('team1_predicted_score', 0)}</p>
                  <p class="text-xs text-slate-400">Predicted</p>
                </div>
                <div class="text-center">
                  <p class="text-sm {confidence_color}">{matchup.get('confidence', 'Medium')} Confidence</p>
                  <p class="text-xs text-slate-400">Winner: {matchup.get('predicted_winner', 'TBD')}</p>
                </div>
                <div class="text-center">
                  <p class="text-2xl font-bold">{matchup.get('team2_predicted_score', 0)}</p>
                  <p class="text-xs text-slate-400">Predicted</p>
                </div>
              </div>
            </div>
            '''
        
        html += '</div></section>'
        return html
    
    def _generate_predictions_section(self, weekly_data: Dict) -> str:
        """Generate predictions section"""
        predictions = weekly_data.get('predictions', {})
        
        html = '''
        <section class="card px-5 sm:px-6 py-6">
          <h2 class="font-header text-3xl sm:text-4xl font-bold text-center mb-6">🔮 This Week's Predictions</h2>
          <div class="grid grid-cols-1 gap-4 lg:grid-cols-2">
        '''
        
        # Upset Alert
        upset = predictions.get('upset_alert', {})
        html += f'''
        <div class="sub-card p-4 border border-yellow-500/30">
          <h3 class="font-header text-xl text-yellow-400 mb-3">🚨 Upset Alert</h3>
          <p class="text-sm">{upset.get('team1', 'Team 1')} vs {upset.get('team2', 'Team 2')}</p>
          <p class="text-xs text-slate-400">The underdog could pull off the upset this week</p>
        </div>
        '''
        
        # Blowout of the Week
        blowout = predictions.get('blowout_of_the_week', {})
        html += f'''
        <div class="sub-card p-4 border border-red-500/30">
          <h3 class="font-header text-xl text-red-400 mb-3">💥 Blowout of the Week</h3>
          <p class="text-sm">{blowout.get('team1', 'Team 1')} vs {blowout.get('team2', 'Team 2')}</p>
          <p class="text-xs text-slate-400">This one could get ugly fast</p>
        </div>
        '''
        
        # Closest Matchup
        closest = predictions.get('closest_matchup', {})
        html += f'''
        <div class="sub-card p-4 border border-blue-500/30">
          <h3 class="font-header text-xl text-blue-400 mb-3">⚡ Closest Matchup</h3>
          <p class="text-sm">{closest.get('team1', 'Team 1')} vs {closest.get('team2', 'Team 2')}</p>
          <p class="text-xs text-slate-400">This one could go either way</p>
        </div>
        '''
        
        # Highest Scorer
        highest = predictions.get('highest_scorer', {})
        html += f'''
        <div class="sub-card p-4 border border-green-500/30">
          <h3 class="font-header text-xl text-green-400 mb-3">🏆 Highest Scorer</h3>
          <p class="text-sm">{highest.get('team', 'Team')} ({highest.get('owner', 'Owner')})</p>
          <p class="text-xs text-slate-400">Predicted to light up the scoreboard</p>
        </div>
        '''
        
        html += '</div></section>'
        return html
    
    def _generate_storylines_section(self, weekly_data: Dict) -> str:
        """Generate storylines section"""
        storylines = weekly_data.get('storylines', [])
        
        html = '''
        <section class="card px-5 sm:px-6 py-6">
          <h2 class="font-header text-3xl sm:text-4xl font-bold text-center mb-6">📰 Storylines to Watch</h2>
          <div class="space-y-4">
        '''
        
        for storyline in storylines:
            html += f'''
            <div class="sub-card p-4">
              <p class="text-sm">{storyline}</p>
            </div>
            '''
        
        html += '</div></section>'
        return html
    
    def _generate_waiver_section(self, weekly_data: Dict) -> str:
        """Generate waiver wire section"""
        waiver_picks = weekly_data.get('waiver_wire', [])
        
        html = '''
        <section class="card px-5 sm:px-6 py-6">
          <h2 class="font-header text-3xl sm:text-4xl font-bold text-center mb-6">🎯 Waiver Wire Picks</h2>
          <div class="grid grid-cols-1 gap-4 lg:grid-cols-2">
        '''
        
        for pick in waiver_picks:
            html += f'''
            <div class="sub-card p-4">
              <div class="flex justify-between items-start mb-2">
                <div>
                  <p class="font-bold">{pick.get('player', 'Player')} ({pick.get('position', 'POS')})</p>
                  <p class="text-sm text-slate-400">{pick.get('team', 'FA')}</p>
                </div>
                <span class="text-xs bg-blue-900/30 px-2 py-1 rounded">{pick.get('faab_suggestion', 0)} FAAB</span>
              </div>
              <p class="text-xs text-slate-400">{pick.get('reason', 'Good pickup')}</p>
            </div>
            '''
        
        html += '</div></section>'
        return html
    
    def _generate_weather_section(self, weekly_data: Dict) -> str:
        """Generate weather watch section"""
        weather_impacts = weekly_data.get('weather_watch', [])
        
        html = '''
        <section class="card px-5 sm:px-6 py-6">
          <h2 class="font-header text-3xl sm:text-4xl font-bold text-center mb-6">🌤️ Weather Watch</h2>
          <div class="space-y-4">
        '''
        
        for weather in weather_impacts:
            html += f'''
            <div class="sub-card p-4">
              <div class="flex justify-between items-center mb-2">
                <p class="font-bold">{weather.get('city', 'City')}</p>
                <span class="text-sm text-slate-400">{weather.get('condition', 'Clear')}</span>
              </div>
              <p class="text-sm text-slate-400">{weather.get('impact', 'No impact')}</p>
              <p class="text-xs text-slate-500">{weather.get('games_affected', 0)} games affected</p>
            </div>
            '''
        
        html += '</div></section>'
        return html
    
    def _generate_injury_section(self, weekly_data: Dict) -> str:
        """Generate injury report section"""
        injuries = weekly_data.get('injury_report', [])
        
        html = '''
        <section class="card px-5 sm:px-6 py-6">
          <h2 class="font-header text-3xl sm:text-4xl font-bold text-center mb-6">🏥 Injury Report</h2>
          <div class="space-y-4">
        '''
        
        for injury in injuries:
            impact_color = {
                "High": "text-red-400",
                "Medium": "text-yellow-400",
                "Low": "text-green-400"
            }.get(injury.get('impact', 'Medium'), 'text-yellow-400')
            
            html += f'''
            <div class="sub-card p-4">
              <div class="flex justify-between items-center mb-2">
                <p class="font-bold">{injury.get('player', 'Player')}</p>
                <span class="text-sm {impact_color}">{injury.get('status', 'Questionable')}</span>
              </div>
              <p class="text-xs text-slate-400">Impact: {injury.get('impact', 'Medium')}</p>
            </div>
            '''
        
        html += '</div></section>'
        return html
    
    def _generate_preweek_roasts(self, weekly_data: Dict) -> str:
        """Generate pre-week roasting section"""
        matchups = weekly_data.get('matchups', [])
        
        html = '''
        <section class="card px-5 sm:px-6 py-6 border-2 border-red-600/50">
          <h2 class="font-header text-3xl sm:text-4xl font-bold text-center text-red-400">🔥 PRE-GAME TRASH TALK 🔥</h2>
          <div class="mt-6 space-y-4">
        '''
        
        # Generate pre-game roasts for each matchup
        for matchup in matchups[:4]:  # Top 4 matchups
            team1 = matchup.get('team1', 'Team 1')
            team2 = matchup.get('team2', 'Team 2')
            
            roast = self._generate_preweek_matchup_roast(matchup)
            
            html += f'''
            <div class="sub-card p-4 border border-red-500/30">
              <h3 class="font-header text-xl text-red-300 mb-3">{team1} vs {team2}</h3>
              <p class="text-sm">{roast}</p>
            </div>
            '''
        
        html += '</div></section>'
        return html
    
    def _generate_preweek_matchup_roast(self, matchup: Dict) -> str:
        """Generate a pre-game roast for a matchup"""
        team1 = matchup.get('team1', 'Team 1')
        team2 = matchup.get('team2', 'Team 2')
        score1 = matchup.get('team1_predicted_score', 0)
        score2 = matchup.get('team2_predicted_score', 0)
        confidence = matchup.get('confidence', 'Medium')
        
        preweek_roasts = [
            f"{team1} is predicted to score {score1} points while {team2} gets {score2}. {confidence} confidence this prediction is right, but we all know anything can happen.",
            f"The battle between {team1} and {team2} could be the game of the week. Or it could be a complete snoozefest. Only time will tell.",
            f"{team1} vs {team2} - one team will win, one team will lose, and both will probably complain about their luck.",
            f"Predicted score: {team1} {score1}, {team2} {score2}. But let's be honest, these predictions are about as reliable as a weather forecast.",
            f"{team1} and {team2} face off this week. May the best team win, and may the worst team have a good excuse ready.",
            f"The matchup between {team1} and {team2} is {confidence.lower()} confidence. That means there's a {random.randint(30, 70)}% chance we're completely wrong."
        ]
        
        return random.choice(preweek_roasts)
    
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
            "standings": []
        }

def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate pre-week fantasy football newsletter')
    parser.add_argument('--week', type=int, required=True, help='Week number to generate preview for')
    parser.add_argument('--title', help='Custom title for the newsletter')
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = PreWeekNewsletterGenerator()
    
    try:
        # Generate newsletter
        output_file = generator.generate_preweek_newsletter(args.week, args.title)
        print(f"✅ Pre-week newsletter generated successfully!")
        
    except Exception as e:
        print(f"❌ Error generating pre-week newsletter: {e}")
        raise

if __name__ == "__main__":
    main()
