#!/usr/bin/env python3
"""
Simple Pre-Week Newsletter Generator
Focuses on engagement with minimal data requirements
"""

import os
import json
import random
from datetime import datetime
from jinja2 import Template
from typing import Dict, List, Any, Optional

class SimplePreWeekNewsletterGenerator:
    def __init__(self):
        self.data_dir = "data"
        self.template_file = "preweek-template.html"
        
    def generate_preweek_newsletter(self, week_number: int, title: str = None) -> str:
        """Generate a simple pre-week newsletter"""
        print(f"📰 Generating simple pre-week newsletter for Week {week_number}...")
        
        # Load data
        weekly_data = self._load_weekly_data(week_number)
        season_data = self._load_season_data()
        
        if not weekly_data:
            print("❌ No weekly data found, generating mock data...")
            weekly_data = self._generate_mock_weekly_data(week_number)
        
        # Generate title if not provided
        if not title:
            title = self._generate_simple_title(week_number)
        
        # Load template
        template_content = self._load_template()
        if not template_content:
            raise FileNotFoundError(f"Template file not found: {self.template_file}")
        
        # Generate content
        content = self._populate_template(template_content, week_number, title, weekly_data, season_data)
        
        # Save newsletter
        output_file = f"preweek-{week_number:02d}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Simple pre-week newsletter generated: {output_file}")
        print(f"📁 Saved to: {os.path.abspath(output_file)}")
        
        return output_file
    
    def _load_weekly_data(self, week_number: int) -> Dict:
        """Load weekly data, fallback to latest available week"""
        weekly_file = os.path.join(self.data_dir, "weekly", f"week-{week_number:02d}.json")
        
        if os.path.exists(weekly_file):
            with open(weekly_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Try to find latest available week
        latest_week = self._find_latest_weekly_data()
        if latest_week:
            print(f"📊 Using data from Week {latest_week} for standings preview")
            weekly_file = os.path.join(self.data_dir, "weekly", f"week-{latest_week:02d}.json")
            with open(weekly_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return None
    
    def _find_latest_weekly_data(self) -> int:
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
    
    def _load_season_data(self) -> Dict:
        """Load season data"""
        season_file = os.path.join(self.data_dir, "season-stats.json")
        if os.path.exists(season_file):
            with open(season_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _load_template(self) -> str:
        """Load HTML template"""
        if os.path.exists(self.template_file):
            with open(self.template_file, 'r', encoding='utf-8') as f:
                return f.read()
        return None
    
    def _generate_mock_weekly_data(self, week_number: int) -> Dict:
        """Generate mock weekly data for testing"""
        return {
            "week": week_number,
            "season": 2025,
            "standings": [
                {"owner": "healzyswarriors", "wins": 2, "losses": 0, "points_for": 216.64, "points_against": 184.32},
                {"owner": "Wicka", "wins": 2, "losses": 0, "points_for": 198.45, "points_against": 175.23},
                {"owner": "FattyC26", "wins": 1, "losses": 1, "points_for": 185.32, "points_against": 192.15},
                {"owner": "gunga36", "wins": 0, "losses": 2, "points_for": 165.78, "points_against": 201.45}
            ]
        }
    
    def _generate_simple_title(self, week_number: int) -> str:
        """Generate a simple, engaging title"""
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
        standings_section = self._generate_standings_preview(weekly_data)
        matchups_section = self._generate_matchups_preview(weekly_data)
        storylines_section = self._generate_storylines_section(weekly_data)
        roasting_section = self._generate_simple_roasts(weekly_data)
        
        # Replace template placeholders
        template = Template(template_content)
        return template.render(
            week_number=week_number,
            week_title=week_title,
            current_date=datetime.now().strftime("%B %d, %Y"),
            standings_section=standings_section,
            matchups_section=matchups_section,
            storylines_section=storylines_section,
            roasting_section=roasting_section
        )
    
    def _generate_standings_preview(self, weekly_data: Dict) -> str:
        """Generate a simple standings preview focusing on key storylines"""
        standings = weekly_data.get('standings', [])
        if not standings:
            return "<p>No standings data available for preview.</p>"
        
        # Get top 3 and bottom 3 teams for quick storylines
        top_teams = standings[:3]
        bottom_teams = standings[-3:]
        
        html = "<div class='mb-8'>"
        html += "<h2 class='text-2xl font-bold text-gray-800 mb-4'>🏆 Current Standings Preview</h2>"
        
        # Top teams storylines
        html += "<div class='mb-6'>"
        html += "<h3 class='text-lg font-semibold text-green-600 mb-2'>🔥 Hot Teams</h3>"
        for i, team in enumerate(top_teams, 1):
            owner = team.get('owner', 'Unknown')
            wins = team.get('wins', 0)
            losses = team.get('losses', 0)
            
            if wins == 0 and losses == 0:
                storyline = f"<strong>{owner}</strong> is off to a perfect start! Can they keep the momentum?"
            elif wins > losses:
                storyline = f"<strong>{owner}</strong> is {wins}-{losses} and looking strong. Will they stay on top?"
            else:
                storyline = f"<strong>{owner}</strong> is {wins}-{losses} but has potential. Time to turn it around?"
            
            html += f"<p class='text-gray-700 mb-2'>{storyline}</p>"
        html += "</div>"
        
        # Bottom teams storylines
        html += "<div class='mb-6'>"
        html += "<h3 class='text-lg font-semibold text-red-600 mb-2'>⚠️ Teams to Watch</h3>"
        for team in bottom_teams:
            owner = team.get('owner', 'Unknown')
            wins = team.get('wins', 0)
            losses = team.get('losses', 0)
            
            if wins == 0:
                storyline = f"<strong>{owner}</strong> is still looking for their first win. This could be the week!"
            else:
                storyline = f"<strong>{owner}</strong> is {wins}-{losses} and needs a big week to stay in contention."
            
            html += f"<p class='text-gray-700 mb-2'>{storyline}</p>"
        html += "</div>"
        
        html += "</div>"
        return html
    
    def _generate_matchups_preview(self, weekly_data: Dict) -> str:
        """Generate matchup previews using upcoming matchups or standings fallback"""
        # Try to get upcoming matchups first
        upcoming_matchups = self._get_upcoming_matchups(weekly_data.get('week', 1) + 1)
        
        if upcoming_matchups:
            return self._generate_upcoming_matchups_preview(upcoming_matchups)
        else:
            return self._generate_standings_based_matchups_preview(weekly_data)
    
    def _get_upcoming_matchups(self, week_number: int) -> List[Dict]:
        """Get upcoming matchups from file or generate them"""
        # Try to load from file first
        upcoming_file = os.path.join(self.data_dir, "weekly", f"upcoming-week-{week_number:02d}.json")
        if os.path.exists(upcoming_file):
            with open(upcoming_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('matchups', [])
        
        # Generate matchups based on current standings
        return self._generate_standings_based_matchups(week_number)
    
    def _generate_standings_based_matchups(self, week_number: int) -> List[Dict]:
        """Generate matchups based on current standings"""
        standings = self._load_current_standings()
        if not standings:
            return []
        
        matchups = []
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
                    }
                }
                matchups.append(matchup)
        
        return matchups
    
    def _load_current_standings(self) -> List[Dict]:
        """Load current standings from latest weekly data"""
        latest_week = self._find_latest_weekly_data()
        if latest_week:
            weekly_file = os.path.join(self.data_dir, "weekly", f"week-{latest_week:02d}.json")
            if os.path.exists(weekly_file):
                with open(weekly_file, 'r', encoding='utf-8') as f:
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
    
    def _generate_upcoming_matchups_preview(self, matchups: List[Dict]) -> str:
        """Generate preview using real upcoming matchups"""
        html = "<div class='mb-8'>"
        html += "<h2 class='text-2xl font-bold text-gray-800 mb-4'>⚔️ This Week's Matchups</h2>"
        
        for matchup in matchups:
            team1 = matchup['team1']
            team2 = matchup['team2']
            
            owner1 = team1.get('owner', 'Unknown')
            owner2 = team2.get('owner', 'Unknown')
            
            # Get records if available
            wins1 = team1.get('wins', 0)
            losses1 = team1.get('losses', 0)
            wins2 = team2.get('wins', 0)
            losses2 = team2.get('losses', 0)
            
            # Get projected points if available
            proj1 = team1.get('projected_points', 0)
            proj2 = team2.get('projected_points', 0)
            
            # Create storyline
            if wins1 > wins2:
                storyline = f"<strong>{owner1}</strong> ({wins1}-{losses1}) vs <strong>{owner2}</strong> ({wins2}-{losses2}) - Can {owner2} pull off the upset?"
            elif wins2 > wins1:
                storyline = f"<strong>{owner1}</strong> ({wins1}-{losses1}) vs <strong>{owner2}</strong> ({wins2}-{losses2}) - Can {owner1} turn the tables?"
            else:
                storyline = f"<strong>{owner1}</strong> ({wins1}-{losses1}) vs <strong>{owner2}</strong> ({wins2}-{losses2}) - Evenly matched battle!"
            
            # Add projected points if available
            if proj1 > 0 and proj2 > 0:
                storyline += f"<br><span class='text-sm text-gray-600'>Projected: {owner1} {proj1:.1f} - {owner2} {proj2:.1f}</span>"
            
            html += f"<div class='bg-gray-50 p-4 rounded-lg mb-4'>"
            html += f"<p class='text-gray-800'>{storyline}</p>"
            html += "</div>"
        
        html += "</div>"
        return html
    
    def _generate_standings_based_matchups_preview(self, weekly_data: Dict) -> str:
        """Generate matchup previews based on current standings (fallback)"""
        standings = weekly_data.get('standings', [])
        if not standings:
            return "<p>No standings data available for matchup preview.</p>"
        
        # Create simple matchups based on standings
        matchups = []
        for i in range(0, len(standings), 2):
            if i + 1 < len(standings):
                team1 = standings[i]
                team2 = standings[i + 1]
                matchups.append((team1, team2))
        
        html = "<div class='mb-8'>"
        html += "<h2 class='text-2xl font-bold text-gray-800 mb-4'>⚔️ This Week's Matchups</h2>"
        
        for team1, team2 in matchups:
            owner1 = team1.get('owner', 'Unknown')
            owner2 = team2.get('owner', 'Unknown')
            wins1 = team1.get('wins', 0)
            losses1 = team1.get('losses', 0)
            wins2 = team2.get('wins', 0)
            losses2 = team2.get('losses', 0)
            
            # Simple storyline based on records
            if wins1 > wins2:
                storyline = f"<strong>{owner1}</strong> ({wins1}-{losses1}) vs <strong>{owner2}</strong> ({wins2}-{losses2}) - Can {owner2} pull off the upset?"
            elif wins2 > wins1:
                storyline = f"<strong>{owner1}</strong> ({wins1}-{losses1}) vs <strong>{owner2}</strong> ({wins2}-{losses2}) - Can {owner1} turn the tables?"
            else:
                storyline = f"<strong>{owner1}</strong> ({wins1}-{losses1}) vs <strong>{owner2}</strong> ({wins2}-{losses2}) - Evenly matched battle!"
            
            html += f"<div class='bg-gray-50 p-4 rounded-lg mb-4'>"
            html += f"<p class='text-gray-800'>{storyline}</p>"
            html += "</div>"
        
        html += "</div>"
        return html
    
    def _generate_storylines_section(self, weekly_data: Dict) -> str:
        """Generate engaging storylines from current data"""
        standings = weekly_data.get('standings', [])
        if not standings:
            return "<p>No data available for storylines.</p>"
        
        html = "<div class='mb-8'>"
        html += "<h2 class='text-2xl font-bold text-gray-800 mb-4'>📰 This Week's Storylines</h2>"
        
        # Generate storylines from current standings
        storylines = []
        
        # Perfect record storyline
        perfect_teams = [team for team in standings if team.get('wins', 0) > 0 and team.get('losses', 0) == 0]
        if perfect_teams:
            storylines.append(f"<strong>{perfect_teams[0].get('owner', 'Unknown')}</strong> is the only undefeated team. Can they keep it going?")
        
        # Winless team storyline
        winless_teams = [team for team in standings if team.get('wins', 0) == 0]
        if winless_teams:
            storylines.append(f"<strong>{winless_teams[0].get('owner', 'Unknown')}</strong> is still looking for their first win. This could be the week!")
        
        # Division race storyline
        storylines.append("The division title race is heating up as we enter the crucial mid-season stretch")
        
        # Waiver wire storyline
        storylines.append("The waiver wire is buzzing with potential game-changers this week")
        
        for storyline in storylines:
            html += f"<p class='text-gray-700 mb-3'>{storyline}</p>"
        
        html += "</div>"
        return html
    
    def _generate_simple_roasts(self, weekly_data: Dict) -> str:
        """Generate simple pre-week roasts"""
        standings = weekly_data.get('standings', [])
        if not standings:
            return "<p>No data available for roasts.</p>"
        
        html = "<div class='mb-8'>"
        html += "<h2 class='text-2xl font-bold text-gray-800 mb-4'>🔥 Pre-Week Roasts</h2>"
        
        # Simple roasts based on current performance
        roasts = []
        
        # Top team roast
        if standings:
            top_team = standings[0]
            owner = top_team.get('owner', 'Unknown')
            roasts.append(f"<strong>{owner}</strong> is on top... for now. The pressure is on to stay there!")
        
        # Bottom team roast
        if len(standings) > 1:
            bottom_team = standings[-1]
            owner = bottom_team.get('owner', 'Unknown')
            roasts.append(f"<strong>{owner}</strong> is at the bottom, but every week is a chance to climb!")
        
        # General roasts
        roasts.append("Some teams are already planning their playoff strategy, others are just trying to win a game")
        roasts.append("The waiver wire is about to get interesting with some teams desperate for help")
        
        for roast in roasts:
            html += f"<p class='text-gray-700 mb-3'>{roast}</p>"
        
        html += "</div>"
        return html

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate a simple pre-week newsletter')
    parser.add_argument('--week', type=int, required=True, help='Week number')
    parser.add_argument('--title', type=str, help='Custom title for the newsletter')
    
    args = parser.parse_args()
    
    generator = SimplePreWeekNewsletterGenerator()
    output_file = generator.generate_preweek_newsletter(args.week, args.title)
    print(f"✅ Simple pre-week newsletter generated: {output_file}")

if __name__ == "__main__":
    main()
