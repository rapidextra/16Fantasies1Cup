#!/usr/bin/env python3
"""
Fantasy Football Newsletter Generator
Creates HTML newsletter files from weekly data with roasting content
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any
from jinja2 import Template
import sys

# Add parent directory to path to import roasting engine
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from scripts.roasting_engine import RoastingEngine

class NewsletterGenerator:
    def __init__(self):
        self.project_root = os.path.dirname(os.path.dirname(__file__))
        self.data_dir = os.path.join(self.project_root, 'data')
        self.template_file = os.path.join(self.project_root, 'week-template.html')
        self.roasting_engine = RoastingEngine()
        
    def generate_newsletter(self, week_number: int, week_title: str = None) -> str:
        """Generate a complete newsletter for the given week"""
        print(f"Generating newsletter for Week {week_number}...")
        
        # Load data
        weekly_data = self._load_weekly_data(week_number)
        season_data = self._load_season_data()
        
        # Generate title if not provided
        if not week_title:
            week_title = self._generate_week_title(weekly_data)
        
        # Load template
        with open(self.template_file, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Replace placeholders
        newsletter_html = self._populate_template(
            template_content, 
            week_number, 
            week_title, 
            weekly_data, 
            season_data
        )
        
        # Save newsletter file
        output_file = os.path.join(self.project_root, f'week-{week_number:02d}.html')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(newsletter_html)
        
        # Update weeks.js
        self._update_weeks_js(week_number, week_title, weekly_data)
        
        print(f"✅ Newsletter saved as week-{week_number:02d}.html")
        return output_file

    def _load_weekly_data(self, week_number: int) -> Dict:
        """Load weekly data from JSON file"""
        week_file = os.path.join(self.data_dir, 'weekly', f'week-{week_number:02d}.json')
        try:
            with open(week_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._generate_mock_weekly_data(week_number)

    def _load_season_data(self) -> Dict:
        """Load season stats data"""
        season_file = os.path.join(self.data_dir, 'season-stats.json')
        try:
            with open(season_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _generate_week_title(self, weekly_data: Dict) -> str:
        """Generate a catchy title for the week"""
        titles = [
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
        
        week = weekly_data.get('week', 1)
        return titles[week % len(titles)]

    def _populate_template(self, template: str, week_number: int, week_title: str, 
                          weekly_data: Dict, season_data: Dict) -> str:
        """Replace template placeholders with actual content"""
        
        # Basic replacements
        html = template.replace('[WEEK_NUMBER]', str(week_number))
        html = html.replace('[WEEK_TITLE]', week_title)
        
        # Generate main content sections
        standings_section = self._generate_standings_section(weekly_data, season_data)
        matchups_section = self._generate_matchups_section(weekly_data)
        trades_section = self._generate_trades_section(weekly_data)
        roasts_section = self._generate_roasts_section(weekly_data)
        
        # Replace content placeholder
        content_placeholder = '<!-- Your newsletter content goes here -->'
        newsletter_content = f"""
        {standings_section}
        {matchups_section}
        {trades_section}
        {roasts_section}
        """
        
        html = html.replace(content_placeholder, newsletter_content)
        
        # Generate custom poll question
        poll_question = self._generate_poll_question(weekly_data)
        html = html.replace('[POLL QUESTION - customize this for each week]', poll_question)
        
        # Replace poll options
        poll_options = self._generate_poll_options(weekly_data)
        for i, option in enumerate(poll_options, 1):
            html = html.replace(f'[Option {i}]', option)
        
        return html

    def _generate_standings_section(self, weekly_data: Dict, season_data: Dict) -> str:
        """Generate the standings section with roasting commentary"""
        standings = weekly_data.get('standings', [])
        
        html = '''
        <section id="standings" class="card px-5 sm:px-6 py-6">
          <h2 class="font-header text-3xl sm:text-4xl font-bold text-center gold-text">The Table of Glory (and Shame)</h2>
          <p class="mt-1 text-center italic text-slate-400">Where champions rise, pretenders flop, and clowns collect L's.</p>
        '''
        
        # Top 3 contenders
        top_3 = standings[:3]
        if top_3:
            html += '''
            <div class="mt-8 rounded-lg border border-yellow-700/60 bg-yellow-900/20 p-4">
              <h3 class="font-header text-2xl sm:text-3xl text-center mb-3">🏆 Contenders</h3>
              <div class="grid grid-cols-1 gap-4 lg:grid-cols-3">
            '''
            
            for i, team in enumerate(top_3):
                roast = self.roasting_engine.generate_team_roast(team, weekly_data, "contender")
                html += f'''
                <article class="sub-card p-4 text-center">
                  <div class="status-badge badge-contender">Crown Contender</div>
                  <p class="font-bold">{i+1}. {team.get('team', 'Unknown')} ({team.get('record', '0-0')})</p>
                  <p class="mb-2 text-xs text-slate-400">PF: #{team.get('rank_pf', '?')} · PA: {self._format_pa_ranking(team)} · {team.get('streak', '')}</p>
                  <p class="text-sm">{roast}</p>
                </article>
                '''
            
            html += '</div></div>'
        
        # Bubble teams (4-8)
        bubble_teams = standings[3:8] if len(standings) > 3 else []
        if bubble_teams:
            html += '''
            <div class="mt-6 rounded-lg border border-blue-700/60 bg-blue-900/20 p-4">
              <h3 class="font-header text-2xl sm:text-3xl text-center mb-3">⚡ Bubble Watch</h3>
              <div class="grid grid-cols-1 gap-3 lg:grid-cols-2">
            '''
            
            for i, team in enumerate(bubble_teams, 4):
                roast = self.roasting_engine.generate_team_roast(team, weekly_data, "bubble")
                html += f'''
                <article class="sub-card p-3 text-center">
                  <div class="status-badge badge-chaser">Playoff Chaser</div>
                  <p class="font-bold">{i}. {team.get('team', 'Unknown')} ({team.get('record', '0-0')})</p>
                  <p class="text-xs">{roast}</p>
                </article>
                '''
            
            html += '</div></div>'
        
        html += '</section>'
        return html

    def _generate_matchups_section(self, weekly_data: Dict) -> str:
        """Generate the weekly matchups section"""
        matchups = weekly_data.get('matchups', [])
        
        html = '''
        <section class="card px-5 sm:px-6 py-6">
          <h2 class="font-header text-3xl sm:text-4xl font-bold text-center gold-text">⚔️ This Week's Carnage</h2>
          <div class="mt-6 space-y-4">
        '''
        
        for matchup in matchups[:6]:  # Show top 6 matchups
            winner = matchup.get('winner', matchup.get('team1', ''))
            loser = matchup.get('team2', '') if winner == matchup.get('team1', '') else matchup.get('team1', '')
            
            roast = self.roasting_engine.generate_matchup_roast(matchup)
            
            html += f'''
            <div class="sub-card p-4">
              <div class="flex justify-between items-center mb-2">
                <span class="font-bold text-green-400">{winner}</span>
                <span class="text-slate-400">vs</span>
                <span class="font-bold text-red-400">{loser}</span>
              </div>
              <div class="text-center text-2xl font-bold mb-2">
                {matchup.get('team1_score', 0)} - {matchup.get('team2_score', 0)}
              </div>
              <p class="text-sm text-slate-300 italic text-center">{roast}</p>
            </div>
            '''
        
        html += '</div></section>'
        return html

    def _generate_trades_section(self, weekly_data: Dict) -> str:
        """Generate the trades and transactions section"""
        transactions = weekly_data.get('transactions', [])
        trades = [t for t in transactions if t.get('type') == 'trade']
        waivers = [t for t in transactions if t.get('type') == 'waiver']
        
        if not trades and not waivers:
            return ""
        
        html = '''
        <section class="card px-5 sm:px-6 py-6">
          <h2 class="font-header text-3xl sm:text-4xl font-bold text-center gold-text">💼 Wheelin' and Dealin'</h2>
        '''
        
        if trades:
            html += '<h3 class="font-header text-2xl text-yellow-400 mt-6 mb-3">🔄 Trade Analysis</h3>'
            for trade in trades:
                analysis = trade.get('analysis', 'Even trade')
                html += f'''
                <div class="sub-card p-4 mb-3">
                  <div class="font-semibold mb-2">{' ↔ '.join(trade.get('teams', []))}</div>
                  <div class="text-sm text-slate-300">{', '.join(trade.get('players_traded', []))}</div>
                  <div class="text-xs text-slate-400 mt-2 italic">{analysis}</div>
                </div>
                '''
        
        if waivers:
            html += '<h3 class="font-header text-2xl text-yellow-400 mt-6 mb-3">💰 Waiver Wire Winners</h3>'
            for waiver in waivers:
                html += f'''
                <div class="sub-card p-3 mb-2">
                  <div class="flex justify-between">
                    <span>{waiver.get('team', 'Unknown')} claimed {waiver.get('player', 'Unknown')}</span>
                    <span class="text-green-400">${waiver.get('faab_spent', 0)}</span>
                  </div>
                </div>
                '''
        
        html += '</section>'
        return html

    def _generate_roasts_section(self, weekly_data: Dict) -> str:
        """Generate the enhanced roasting section"""
        html = '''
        <section class="card px-5 sm:px-6 py-6 border-2 border-red-600/50">
          <h2 class="font-header text-3xl sm:text-4xl font-bold text-center text-red-400">🔥 WEEKLY ROAST CORNER 🔥</h2>
          <div class="mt-6 space-y-4">
        '''
        
        # Generate enhanced roasts
        roasts = self._generate_enhanced_roasts(weekly_data)
        
        for category, roast_list in roasts.items():
            html += f'''
            <div class="sub-card p-4 border border-red-500/30">
              <h3 class="font-header text-xl text-red-300 mb-3">{category}</h3>
              <div class="space-y-2">
            '''
            
            for roast in roast_list:
                html += f'<div class="bg-red-900/30 p-3 rounded text-sm">{roast}</div>'
            
            html += '</div></div>'
        
        html += '</div></section>'
        return html

    def _generate_enhanced_roasts(self, weekly_data: Dict) -> Dict[str, List[str]]:
        """Generate enhanced roasts using the roasting engine"""
        standings = weekly_data.get('standings', [])
        matchups = weekly_data.get('matchups', [])
        transactions = weekly_data.get('transactions', {})
        
        roasts = {
            "🏆 Top Performers Getting Roasted": [],
            "💀 Bottom Feeders Getting Destroyed": [],
            "🤡 Questionable Decisions": [],
            "🔥 League-Wide Shame": []
        }
        
        # Generate team-specific roasts
        for team in standings[:4]:  # Top 4 teams
            roast = self.roasting_engine.generate_team_roast(team, weekly_data, "contender")
            roasts["🏆 Top Performers Getting Roasted"].append(roast)
        
        for team in standings[-4:]:  # Bottom 4 teams
            roast = self.roasting_engine.generate_team_roast(team, weekly_data, "basement")
            roasts["💀 Bottom Feeders Getting Destroyed"].append(roast)
        
        # Generate matchup roasts
        for matchup in matchups[:3]:  # Top 3 matchups
            roast = self.roasting_engine.generate_matchup_roast(matchup)
            roasts["🤡 Questionable Decisions"].append(roast)
        
        # Generate transaction roasts
        for trade in transactions:
            if trade.get('type') == 'trade':
                roast = self.roasting_engine.generate_transaction_roast(trade, "trade")
                roasts["🤡 Questionable Decisions"].append(roast)
        
        for waiver in transactions:
            if waiver.get('type') == 'waiver':
                roast = self.roasting_engine.generate_transaction_roast(waiver, "waiver")
                roasts["🤡 Questionable Decisions"].append(roast)
        
        # Generate league-wide roast
        league_roast = self.roasting_engine.generate_league_roast(weekly_data)
        roasts["🔥 League-Wide Shame"].append(league_roast)
        
        # Remove empty categories
        roasts = {k: v for k, v in roasts.items() if v}
        
        return roasts


    def _format_pa_ranking(self, team: Dict) -> str:
        """Format points against ranking"""
        pa_rank = team.get('pa_rank', 0)
        if pa_rank <= 3:
            return f"{pa_rank}nd easiest"
        elif pa_rank >= 14:
            return f"#{pa_rank} hardest"
        else:
            return f"#{pa_rank} PA"

    def _generate_poll_question(self, weekly_data: Dict) -> str:
        """Generate a relevant poll question for the week"""
        questions = [
            "Who will win the championship this year?",
            "Which team made the worst trade this week?",
            "Who's getting eliminated first in the playoffs?",
            "Most overrated team in the league?",
            "Which owner makes the most questionable decisions?",
            "Who has the best waiver wire luck?",
            "Which team is due for a massive collapse?"
        ]
        
        week = weekly_data.get('week', 1)
        return questions[week % len(questions)]

    def _generate_poll_options(self, weekly_data: Dict) -> List[str]:
        """Generate poll options based on weekly data"""
        standings = weekly_data.get('standings', [])
        top_teams = [team.get('team', f'Team {i}') for i, team in enumerate(standings[:4], 1)]
        
        # Ensure we have 4 options
        while len(top_teams) < 4:
            top_teams.append(f"Team {len(top_teams) + 1}")
        
        return top_teams

    def _update_weeks_js(self, week_number: int, week_title: str, weekly_data: Dict) -> None:
        """Update the weeks.js file with the new week"""
        weeks_file = os.path.join(self.project_root, 'weeks.js')
        
        try:
            with open(weeks_file, 'r') as f:
                content = f.read()
        except FileNotFoundError:
            content = 'window.CUP_WEEKS = []'
        
        # Generate blurb from weekly data
        blurb = self._generate_week_blurb(weekly_data)
        
        # Create new week entry
        new_week = f'''  {{
    week: {week_number},
    slug: 'week-{week_number:02d}',
    title: '{week_title}',
    blurb: '{blurb}'
  }}'''
        
        # Insert into weeks array
        if 'window.CUP_WEEKS = [' in content:
            # Find the array and add the new week
            array_start = content.find('[')
            array_content = content[array_start+1:content.find('].reverse()')]
            
            if array_content.strip():
                new_array = f"[\n{new_week},\n{array_content}\n].reverse();"
            else:
                new_array = f"[\n{new_week}\n].reverse();"
            
            new_content = content[:array_start] + new_array
        else:
            new_content = f'window.CUP_WEEKS = [\n{new_week}\n].reverse();'
        
        with open(weeks_file, 'w') as f:
            f.write(new_content)

    def _generate_week_blurb(self, weekly_data: Dict) -> str:
        """Generate a short blurb describing the week"""
        standings = weekly_data.get('standings', [])
        if standings:
            leader = standings[0].get('team', 'Unknown')
            return f"Week {weekly_data.get('week', '?')} recap — {leader} stays on top, trades heat up, playoff race tightens."
        return f"Week {weekly_data.get('week', '?')} recap — standings, matchups, and roasting material."

    def _generate_mock_weekly_data(self, week_number: int) -> Dict:
        """Generate mock data if weekly data file doesn't exist"""
        return {
            "week": week_number,
            "season": 2024,
            "standings": [
                {"team": "JewTeam", "record": "8-1", "rank": 1, "streak": "W4"},
                {"team": "gunga36", "record": "7-2", "rank": 2, "streak": "W2"},
                {"team": "Bonzo22", "record": "6-3", "rank": 3, "streak": "W1"}
            ],
            "matchups": [
                {"team1": "JewTeam", "team2": "Opponent", "team1_score": 167.3, "team2_score": 134.5, "winner": "JewTeam"}
            ],
            "transactions": {"trades": [], "waivers": []},
            "last_updated": datetime.now().isoformat()
        }

def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate fantasy football newsletter')
    parser.add_argument('--week', type=int, required=True, help='Week number')
    parser.add_argument('--title', help='Custom week title')
    
    args = parser.parse_args()
    
    generator = NewsletterGenerator()
    output_file = generator.generate_newsletter(args.week, args.title)
    
    print(f"📰 Newsletter generated successfully!")
    print(f"📁 Saved to: {output_file}")

if __name__ == "__main__":
    main()