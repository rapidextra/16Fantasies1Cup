#!/usr/bin/env python3
"""
Comprehensive Pre-Week Newsletter Generator
Includes detailed team writeups, unique predictions, trade analysis, and waiver wire activity
"""

import os
import json
import random
from datetime import datetime
from jinja2 import Template
from typing import Dict, List, Any, Optional

class ComprehensivePreWeekNewsletterGenerator:
    def __init__(self):
        self.data_dir = "data"
        self.template_file = "comprehensive-preweek-template.html"
        
    def generate_preweek_newsletter(self, week_number: int, title: str = None) -> str:
        """Generate a comprehensive pre-week newsletter"""
        print(f"📰 Generating comprehensive pre-week newsletter for Week {week_number}...")
        
        # Load data
        weekly_data = self._load_weekly_data(week_number)
        season_data = self._load_season_data()
        
        if not weekly_data:
            print("❌ No weekly data found, generating mock data...")
            weekly_data = self._generate_mock_weekly_data(week_number)
        
        # Generate title if not provided
        if not title:
            title = self._generate_comprehensive_title(week_number)
        
        # Load template
        template_content = self._load_template()
        if not template_content:
            raise FileNotFoundError(f"Template file not found: {self.template_file}")
        
        # Generate content
        content = self._populate_template(template_content, week_number, title, weekly_data, season_data)
        
        # Save newsletter
        output_file = f"comprehensive-preweek-{week_number:02d}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Comprehensive pre-week newsletter generated: {output_file}")
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
    
    def _generate_comprehensive_title(self, week_number: int) -> str:
        """Generate a comprehensive title"""
        titles = [
            "The Deep Dive: Week {} Analysis",
            "Comprehensive Week {} Preview",
            "The Complete Week {} Breakdown",
            "Week {}: The Full Picture",
            "Deep Analysis: Week {} Preview",
            "The Week {} Deep Dive",
            "Complete Week {} Analysis",
            "Week {}: The Comprehensive Guide"
        ]
        return random.choice(titles).format(week_number)
    
    def _populate_template(self, template_content: str, week_number: int, week_title: str, 
                          weekly_data: Dict, season_data: Dict) -> str:
        """Populate the template with data"""
        
        # Generate sections
        standings_section = self._generate_standings_preview(weekly_data)
        team_writeups_section = self._generate_team_writeups(weekly_data)
        matchups_section = self._generate_detailed_matchups(weekly_data)
        predictions_section = self._generate_unique_predictions(weekly_data)
        trades_section = self._generate_trade_analysis(weekly_data)
        waiver_section = self._generate_waiver_analysis(weekly_data)
        watch_for_section = self._generate_watch_for_section(weekly_data)
        storylines_section = self._generate_storylines_section(weekly_data)
        roasting_section = self._generate_comprehensive_roasts(weekly_data)
        
        # Replace template placeholders
        template = Template(template_content)
        return template.render(
            week_number=week_number,
            week_title=week_title,
            current_date=datetime.now().strftime("%B %d, %Y"),
            standings_section=standings_section,
            team_writeups_section=team_writeups_section,
            matchups_section=matchups_section,
            predictions_section=predictions_section,
            trades_section=trades_section,
            waiver_section=waiver_section,
            watch_for_section=watch_for_section,
            storylines_section=storylines_section,
            roasting_section=roasting_section
        )
    
    def _generate_standings_preview(self, weekly_data: Dict) -> str:
        """Generate a detailed standings preview"""
        standings = weekly_data.get('standings', [])
        if not standings:
            return "<p>No standings data available for preview.</p>"
        
        html = "<div class='mb-8'>"
        html += "<h2 class='text-2xl font-bold text-gray-800 mb-4'>🏆 Current Standings Analysis</h2>"
        
        # Top teams analysis
        html += "<div class='mb-6'>"
        html += "<h3 class='text-lg font-semibold text-green-600 mb-2'>🔥 Elite Tier (2-0)</h3>"
        elite_teams = [team for team in standings if team.get('wins', 0) == 2 and team.get('losses', 0) == 0]
        for team in elite_teams:
            owner = team.get('owner', 'Unknown')
            pf = team.get('points_for', 0)
            pa = team.get('points_against', 0)
            diff = pf - pa
            html += f"<p class='text-gray-700 mb-2'><strong>{owner}</strong> - {pf:.1f} PF, {pa:.1f} PA (+{diff:.1f} diff) - Dominating on both sides of the ball</p>"
        html += "</div>"
        
        # Middle tier analysis
        html += "<div class='mb-6'>"
        html += "<h3 class='text-lg font-semibold text-yellow-600 mb-2'>⚖️ Middle Tier (1-1)</h3>"
        middle_teams = [team for team in standings if team.get('wins', 0) == 1 and team.get('losses', 0) == 1]
        for team in middle_teams:
            owner = team.get('owner', 'Unknown')
            pf = team.get('points_for', 0)
            pa = team.get('points_against', 0)
            diff = pf - pa
            html += f"<p class='text-gray-700 mb-2'><strong>{owner}</strong> - {pf:.1f} PF, {pa:.1f} PA ({diff:+.1f} diff) - Inconsistent but dangerous</p>"
        html += "</div>"
        
        # Bottom tier analysis
        html += "<div class='mb-6'>"
        html += "<h3 class='text-lg font-semibold text-red-600 mb-2'>⚠️ Struggling Tier (0-2)</h3>"
        struggling_teams = [team for team in standings if team.get('wins', 0) == 0 and team.get('losses', 0) == 2]
        for team in struggling_teams:
            owner = team.get('owner', 'Unknown')
            pf = team.get('points_for', 0)
            pa = team.get('points_against', 0)
            diff = pf - pa
            html += f"<p class='text-gray-700 mb-2'><strong>{owner}</strong> - {pf:.1f} PF, {pa:.1f} PA ({diff:+.1f} diff) - Needs a breakout week</p>"
        html += "</div>"
        
        html += "</div>"
        return html
    
    def _generate_team_writeups(self, weekly_data: Dict) -> str:
        """Generate detailed team writeups"""
        standings = weekly_data.get('standings', [])
        if not standings:
            return "<p>No standings data available for team writeups.</p>"
        
        html = "<div class='mb-8'>"
        html += "<h2 class='text-2xl font-bold text-gray-800 mb-4'>📝 Team Deep Dives</h2>"
        
        for i, team in enumerate(standings, 1):
            owner = team.get('owner', 'Unknown')
            wins = team.get('wins', 0)
            losses = team.get('losses', 0)
            pf = team.get('points_for', 0)
            pa = team.get('points_against', 0)
            diff = pf - pa
            
            # Generate team analysis
            analysis = self._generate_team_analysis(team, i)
            
            html += f"<div class='bg-gray-50 p-6 rounded-lg mb-4'>"
            html += f"<h3 class='text-lg font-semibold text-gray-800 mb-2'>{i}. {owner} ({wins}-{losses})</h3>"
            html += f"<p class='text-sm text-gray-600 mb-3'>Points For: {pf:.1f} | Points Against: {pa:.1f} | Differential: {diff:+.1f}</p>"
            html += f"<p class='text-gray-700'>{analysis}</p>"
            html += "</div>"
        
        html += "</div>"
        return html
    
    def _generate_team_analysis(self, team: Dict, rank: int) -> str:
        """Generate analysis for a specific team"""
        owner = team.get('owner', 'Unknown')
        wins = team.get('wins', 0)
        losses = team.get('losses', 0)
        pf = team.get('points_for', 0)
        pa = team.get('points_against', 0)
        diff = pf - pa
        
        analyses = []
        
        # Record-based analysis
        if wins == 2 and losses == 0:
            analyses.append("Perfect start to the season with dominant performances on both sides of the ball.")
            analyses.append("The offense is clicking and the defense is making stops when it matters most.")
        elif wins == 1 and losses == 1:
            analyses.append("Inconsistent start but showing flashes of brilliance.")
            analyses.append("Need to find more consistency to make a playoff push.")
        else:
            analyses.append("Rough start but there's still plenty of time to turn things around.")
            analyses.append("The talent is there, just need to put it all together.")
        
        # Points-based analysis
        if pf > 200:
            analyses.append("High-powered offense that can score with anyone.")
        elif pf > 180:
            analyses.append("Solid offensive production with room for improvement.")
        else:
            analyses.append("Offense needs to find its rhythm and start putting up bigger numbers.")
        
        if pa < 180:
            analyses.append("Stingy defense that's keeping opponents in check.")
        elif pa < 200:
            analyses.append("Decent defensive play with some lapses.")
        else:
            analyses.append("Defense needs to tighten up and limit big plays.")
        
        # Differential analysis
        if diff > 30:
            analyses.append("Dominating both sides of the ball with impressive point differential.")
        elif diff > 0:
            analyses.append("Positive differential shows the team is trending in the right direction.")
        else:
            analyses.append("Negative differential indicates the team needs to step up on both sides.")
        
        return " ".join(analyses)
    
    def _generate_detailed_matchups(self, weekly_data: Dict) -> str:
        """Generate detailed matchup analysis"""
        upcoming_matchups = self._get_upcoming_matchups(weekly_data.get('week', 1) + 1)
        
        if not upcoming_matchups:
            return "<p>No upcoming matchups data available.</p>"
        
        html = "<div class='mb-8'>"
        html += "<h2 class='text-2xl font-bold text-gray-800 mb-4'>⚔️ Detailed Matchup Analysis</h2>"
        
        for matchup in upcoming_matchups:
            team1 = matchup['team1']
            team2 = matchup['team2']
            
            owner1 = team1.get('owner', 'Unknown')
            owner2 = team2.get('owner', 'Unknown')
            wins1 = team1.get('wins', 0)
            losses1 = team1.get('losses', 0)
            wins2 = team2.get('wins', 0)
            losses2 = team2.get('losses', 0)
            pf1 = team1.get('points_for', 0)
            pf2 = team2.get('points_for', 0)
            
            # Generate matchup analysis
            analysis = self._generate_matchup_analysis(team1, team2)
            
            html += f"<div class='bg-gray-50 p-6 rounded-lg mb-6'>"
            html += f"<h3 class='text-lg font-semibold text-gray-800 mb-3'>{owner1} ({wins1}-{losses1}) vs {owner2} ({wins2}-{losses2})</h3>"
            html += f"<div class='grid grid-cols-2 gap-4 mb-4'>"
            html += f"<div class='text-center'><p class='text-sm text-gray-600'>Points For</p><p class='text-lg font-bold'>{pf1:.1f}</p></div>"
            html += f"<div class='text-center'><p class='text-sm text-gray-600'>Points For</p><p class='text-lg font-bold'>{pf2:.1f}</p></div>"
            html += "</div>"
            html += f"<p class='text-gray-700'>{analysis}</p>"
            html += "</div>"
        
        html += "</div>"
        return html
    
    def _generate_matchup_analysis(self, team1: Dict, team2: Dict) -> str:
        """Generate detailed analysis for a specific matchup"""
        owner1 = team1.get('owner', 'Unknown')
        owner2 = team2.get('owner', 'Unknown')
        wins1 = team1.get('wins', 0)
        losses1 = team1.get('losses', 0)
        wins2 = team2.get('wins', 0)
        losses2 = team2.get('losses', 0)
        pf1 = team1.get('points_for', 0)
        pf2 = team2.get('points_for', 0)
        
        analysis_parts = []
        
        # Record comparison
        if wins1 > wins2:
            analysis_parts.append(f"{owner1} has the better record and should be favored, but {owner2} can't be counted out.")
        elif wins2 > wins1:
            analysis_parts.append(f"{owner2} has the better record and momentum, but {owner1} will be looking to bounce back.")
        else:
            analysis_parts.append(f"Both teams have identical records, making this a true toss-up.")
        
        # Points comparison
        if pf1 > pf2 + 20:
            analysis_parts.append(f"{owner1} has been significantly more explosive on offense.")
        elif pf2 > pf1 + 20:
            analysis_parts.append(f"{owner2} has been the more consistent scoring team.")
        else:
            analysis_parts.append(f"Both teams have similar offensive production, so defense will be key.")
        
        # Key factors
        if wins1 == 2 and wins2 == 0:
            analysis_parts.append(f"This could be {owner2}'s breakout game against the undefeated {owner1}.")
        elif wins1 == 0 and wins2 == 2:
            analysis_parts.append(f"{owner1} desperately needs a win to get back on track against the hot {owner2}.")
        else:
            analysis_parts.append(f"Both teams have something to prove in this crucial matchup.")
        
        return " ".join(analysis_parts)
    
    def _generate_unique_predictions(self, weekly_data: Dict) -> str:
        """Generate unique predictions for each matchup"""
        upcoming_matchups = self._get_upcoming_matchups(weekly_data.get('week', 1) + 1)
        
        if not upcoming_matchups:
            return "<p>No upcoming matchups data available for predictions.</p>"
        
        html = "<div class='mb-8'>"
        html += "<h2 class='text-2xl font-bold text-gray-800 mb-4'>🔮 Unique Matchup Predictions</h2>"
        
        for matchup in upcoming_matchups:
            team1 = matchup['team1']
            team2 = matchup['team2']
            
            owner1 = team1.get('owner', 'Unknown')
            owner2 = team2.get('owner', 'Unknown')
            
            # Generate unique prediction
            prediction = self._generate_matchup_prediction(team1, team2)
            
            html += f"<div class='bg-blue-50 p-6 rounded-lg mb-4'>"
            html += f"<h3 class='text-lg font-semibold text-blue-800 mb-2'>{owner1} vs {owner2}</h3>"
            html += f"<p class='text-blue-700'>{prediction}</p>"
            html += "</div>"
        
        html += "</div>"
        return html
    
    def _generate_matchup_prediction(self, team1: Dict, team2: Dict) -> str:
        """Generate a unique prediction for a specific matchup"""
        owner1 = team1.get('owner', 'Unknown')
        owner2 = team2.get('owner', 'Unknown')
        wins1 = team1.get('wins', 0)
        wins2 = team2.get('wins', 0)
        pf1 = team1.get('points_for', 0)
        pf2 = team2.get('points_for', 0)
        
        predictions = [
            f"Expect a high-scoring affair with both teams putting up 90+ points. {owner1} has the edge in consistency, but {owner2} could pull off the upset if they get hot early.",
            f"This matchup will come down to the wire, with the winner likely decided by less than 10 points. {owner1} needs to avoid turnovers while {owner2} must capitalize on every opportunity.",
            f"Look for a defensive battle with both teams struggling to find the end zone. The team that makes the fewest mistakes will come out on top in this low-scoring affair.",
            f"Both teams are due for a breakout performance, and this could be the week. Expect fireworks as {owner1} and {owner2} both put up their best numbers of the season.",
            f"This matchup features two teams heading in opposite directions. {owner1} is trending up while {owner2} needs to find answers quickly to avoid falling further behind."
        ]
        
        return random.choice(predictions)
    
    def _generate_trade_analysis(self, weekly_data: Dict) -> str:
        """Generate trade analysis and impact predictions"""
        # This would typically come from transaction data
        # For now, generate mock trade analysis
        
        html = "<div class='mb-8'>"
        html += "<h2 class='text-2xl font-bold text-gray-800 mb-4'>🔄 Trade Analysis & Impact</h2>"
        
        # Mock trade data
        trades = [
            {
                "teams": "healzyswarriors & FattyC26",
                "trade": "RB1 + WR2 for QB1 + TE1",
                "impact": "Both teams addressed key needs, but healzyswarriors got the better end of the deal with the proven RB1.",
                "winner": "healzyswarriors"
            },
            {
                "teams": "Wicka & gunga36",
                "trade": "WR1 for RB2 + 2026 1st",
                "impact": "Wicka gets immediate help at running back while gunga36 builds for the future. Short-term win for Wicka.",
                "winner": "Wicka"
            }
        ]
        
        for trade in trades:
            html += f"<div class='bg-yellow-50 p-6 rounded-lg mb-4'>"
            html += f"<h3 class='text-lg font-semibold text-yellow-800 mb-2'>{trade['teams']}</h3>"
            html += f"<p class='text-sm text-gray-600 mb-2'><strong>Trade:</strong> {trade['trade']}</p>"
            html += f"<p class='text-yellow-700 mb-2'><strong>Impact:</strong> {trade['impact']}</p>"
            html += f"<p class='text-sm font-semibold text-yellow-800'>Winner: {trade['winner']}</p>"
            html += "</div>"
        
        html += "</div>"
        return html
    
    def _generate_waiver_analysis(self, weekly_data: Dict) -> str:
        """Generate waiver wire and free agent analysis"""
        html = "<div class='mb-8'>"
        html += "<h2 class='text-2xl font-bold text-gray-800 mb-4'>📈 Waiver Wire & Free Agent Analysis</h2>"
        
        # Mock waiver wire data
        waiver_picks = [
            {
                "player": "Sleeper RB",
                "position": "RB",
                "team": "FA",
                "reason": "Injury to starter opens opportunity for significant touches",
                "faab_suggestion": 35,
                "impact": "High"
            },
            {
                "player": "Streaming QB",
                "position": "QB",
                "team": "FA",
                "reason": "Favorable matchup against weak secondary",
                "faab_suggestion": 15,
                "impact": "Medium"
            },
            {
                "player": "Handcuff RB",
                "position": "RB",
                "team": "FA",
                "reason": "Insurance policy for your starting RB",
                "faab_suggestion": 8,
                "impact": "Low"
            },
            {
                "player": "Hot WR",
                "position": "WR",
                "team": "FA",
                "reason": "Breakout candidate with increased targets",
                "faab_suggestion": 25,
                "impact": "High"
            }
        ]
        
        html += "<div class='grid grid-cols-1 md:grid-cols-2 gap-4'>"
        for pick in waiver_picks:
            impact_color = "red" if pick["impact"] == "High" else "yellow" if pick["impact"] == "Medium" else "green"
            html += f"<div class='bg-gray-50 p-4 rounded-lg'>"
            html += f"<h4 class='font-semibold text-gray-800'>{pick['player']} ({pick['position']})</h4>"
            html += f"<p class='text-sm text-gray-600 mb-2'>{pick['reason']}</p>"
            html += f"<p class='text-sm'><strong>FAAB Suggestion:</strong> {pick['faab_suggestion']}%</p>"
            html += f"<p class='text-sm'><strong>Impact:</strong> <span class='text-{impact_color}-600 font-semibold'>{pick['impact']}</span></p>"
            html += "</div>"
        html += "</div>"
        
        html += "</div>"
        return html
    
    def _generate_watch_for_section(self, weekly_data: Dict) -> str:
        """Generate what to watch for section"""
        html = "<div class='mb-8'>"
        html += "<h2 class='text-2xl font-bold text-gray-800 mb-4'>👀 What to Watch For</h2>"
        
        watch_items = [
            "Injury reports throughout the week - key players on questionable status could swing matchups",
            "Weather conditions for outdoor games - wind and rain can significantly impact passing games",
            "Thursday night game performance - early week games can set the tone for the entire week",
            "Monday night miracle potential - late games can completely flip the script on Sunday results",
            "Rookie breakouts - first-year players often have their best games in the middle of the season",
            "Veteran comebacks - experienced players sometimes find their rhythm after slow starts",
            "Defensive matchups - some defenses are particularly vulnerable to certain offensive schemes",
            "Coaching adjustments - how teams adapt to recent struggles or build on recent success"
        ]
        
        for item in watch_items:
            html += f"<p class='text-gray-700 mb-2'>• {item}</p>"
        
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
        
        # Trade deadline storyline
        storylines.append("With the trade deadline approaching, teams are making their final moves")
        
        # Rookie storyline
        storylines.append("Several rookies are starting to find their rhythm and could be difference-makers")
        
        for storyline in storylines:
            html += f"<p class='text-gray-700 mb-3'>{storyline}</p>"
        
        html += "</div>"
        return html
    
    def _generate_comprehensive_roasts(self, weekly_data: Dict) -> str:
        """Generate comprehensive pre-week roasts"""
        standings = weekly_data.get('standings', [])
        if not standings:
            return "<p>No data available for roasts.</p>"
        
        html = "<div class='mb-8'>"
        html += "<h2 class='text-2xl font-bold text-gray-800 mb-4'>🔥 Pre-Week Roasts & Analysis</h2>"
        
        # Generate roasts for different tiers
        elite_teams = [team for team in standings if team.get('wins', 0) == 2 and team.get('losses', 0) == 0]
        struggling_teams = [team for team in standings if team.get('wins', 0) == 0 and team.get('losses', 0) == 2]
        
        if elite_teams:
            html += "<div class='mb-4'>"
            html += "<h3 class='text-lg font-semibold text-green-600 mb-2'>🏆 Elite Tier Roasts</h3>"
            for team in elite_teams:
                owner = team.get('owner', 'Unknown')
                html += f"<p class='text-gray-700 mb-2'><strong>{owner}</strong> is on top... for now. The pressure is on to stay there, and everyone's gunning for you!</p>"
            html += "</div>"
        
        if struggling_teams:
            html += "<div class='mb-4'>"
            html += "<h3 class='text-lg font-semibold text-red-600 mb-2'>⚠️ Struggling Tier Roasts</h3>"
            for team in struggling_teams:
                owner = team.get('owner', 'Unknown')
                html += f"<p class='text-gray-700 mb-2'><strong>{owner}</strong> is at the bottom, but every week is a chance to climb! Time to prove the doubters wrong.</p>"
            html += "</div>"
        
        # General roasts
        html += "<div class='mb-4'>"
        html += "<h3 class='text-lg font-semibold text-yellow-600 mb-2'>🎯 General Observations</h3>"
        html += "<p class='text-gray-700 mb-2'>Some teams are already planning their playoff strategy, others are just trying to win a game.</p>"
        html += "<p class='text-gray-700 mb-2'>The waiver wire is about to get interesting with some teams desperate for help.</p>"
        html += "<p class='text-gray-700 mb-2'>This week could make or break several teams' seasons - no pressure!</p>"
        html += "</div>"
        
        html += "</div>"
        return html
    
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

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate a comprehensive pre-week newsletter')
    parser.add_argument('--week', type=int, required=True, help='Week number')
    parser.add_argument('--title', type=str, help='Custom title for the newsletter')
    
    args = parser.parse_args()
    
    generator = ComprehensivePreWeekNewsletterGenerator()
    output_file = generator.generate_preweek_newsletter(args.week, args.title)
    print(f"✅ Comprehensive pre-week newsletter generated: {output_file}")

if __name__ == "__main__":
    main()


