#!/usr/bin/env python3
"""
Enhanced Roasting Engine for 16 Fantasies 1 Cup
Generates dynamic, contextual, and personalized roasts based on performance data
"""

import random
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import sys

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import Config

class RoastingEngine:
    """Advanced roasting system that generates contextual burns"""
    
    def __init__(self):
        self.config = Config()
        self.roast_history = self._load_roast_history()
        self.team_personalities = self._load_team_personalities()
        
    def _load_roast_history(self) -> Dict[str, List[str]]:
        """Load historical roasts to avoid repetition"""
        try:
            with open('data/roast_history.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {team: [] for team in [t['team'] for t in self.config.get_team_config()['teams']]}
    
    def _save_roast_history(self):
        """Save roast history to avoid repetition"""
        os.makedirs('data', exist_ok=True)
        with open('data/roast_history.json', 'w') as f:
            json.dump(self.roast_history, f, indent=2)
    
    def _load_team_personalities(self) -> Dict[str, Dict[str, Any]]:
        """Load team personality profiles for targeted roasting"""
        return {
            "JewTeam": {
                "traits": ["confident", "strategic", "analytical"],
                "weaknesses": ["overthinking", "perfectionist"],
                "catchphrases": ["Lightning strikes twice", "Numbers don't lie"],
                "historical_shame": ["Lost to a team that started a kicker on bye week"]
            },
            "gunga36": {
                "traits": ["aggressive", "risk-taker", "bold"],
                "weaknesses": ["impulsive", "reckless"],
                "catchphrases": ["All or nothing", "Go big or go home"],
                "historical_shame": ["Traded away a top-5 RB for a defense"]
            },
            "Bonzo22": {
                "traits": ["methodical", "patient", "consistent"],
                "weaknesses": ["predictable", "boring"],
                "catchphrases": ["Slow and steady", "Trust the process"],
                "historical_shame": ["Started a player who was declared out 3 hours before kickoff"]
            },
            "healzyswarriors": {
                "traits": ["optimistic", "hopeful", "persistent"],
                "weaknesses": ["delusional", "stubborn"],
                "catchphrases": ["This is our year", "Next week will be different"],
                "historical_shame": ["Dropped a player who scored 30+ the next week"]
            },
            "FattyC26": {
                "traits": ["laid-back", "casual", "unpredictable"],
                "weaknesses": ["inconsistent", "lazy"],
                "catchphrases": ["Whatever happens, happens", "It's just fantasy"],
                "historical_shame": ["Forgot to set lineup for 3 straight weeks"]
            },
            "MorgsLev13": {
                "traits": ["competitive", "intense", "focused"],
                "weaknesses": ["overly serious", "stressed"],
                "catchphrases": ["Every point matters", "No mercy"],
                "historical_shame": ["Lost by 0.1 points due to a stat correction"]
            },
            "coopersallstarz": {
                "traits": ["flashy", "showy", "attention-seeking"],
                "weaknesses": ["arrogant", "overconfident"],
                "catchphrases": ["Look at these moves", "I'm the best"],
                "historical_shame": ["Bragged about a trade that backfired spectacularly"]
            },
            "Stampy": {
                "traits": ["stubborn", "determined", "unyielding"],
                "weaknesses": ["inflexible", "rigid"],
                "catchphrases": ["My way or the highway", "I know what I'm doing"],
                "historical_shame": ["Refused to drop a player who was on IR for 8 weeks"]
            },
            "3whits": {
                "traits": ["mysterious", "enigmatic", "unpredictable"],
                "weaknesses": ["unclear", "confusing"],
                "catchphrases": ["You wouldn't understand", "It's complicated"],
                "historical_shame": ["Made a trade that confused everyone including himself"]
            },
            "webbyt": {
                "traits": ["tech-savvy", "data-driven", "analytical"],
                "weaknesses": ["over-analyzing", "paralysis by analysis"],
                "catchphrases": ["The data says", "Let me check the metrics"],
                "historical_shame": ["Lost because he spent too much time analyzing and forgot to set lineup"]
            },
            "Wicka": {
                "traits": ["lucky", "fortunate", "charmed"],
                "weaknesses": ["overconfident", "reckless"],
                "catchphrases": ["Luck is a skill", "I always win"],
                "historical_shame": ["Lost in the first round of playoffs after talking trash all season"]
            },
            "5yearRebuild": {
                "traits": ["patient", "long-term", "strategic"],
                "weaknesses": ["slow", "indecisive"],
                "catchphrases": ["Trust the process", "Next year is our year"],
                "historical_shame": ["Has been 'rebuilding' for 7 years"]
            },
            "Sedgy": {
                "traits": ["smooth", "charming", "persuasive"],
                "weaknesses": ["manipulative", "sneaky"],
                "catchphrases": ["Let's make a deal", "I have an offer you can't refuse"],
                "historical_shame": ["Tricked someone into trading him their best player for a kicker"]
            },
            "Poddy": {
                "traits": ["loud", "boisterous", "energetic"],
                "weaknesses": ["annoying", "overbearing"],
                "catchphrases": ["LET'S GO!", "I'M HYPED!"],
                "historical_shame": ["Celebrated a win before the game was over and lost by 0.5 points"]
            },
            "DaksDemons": {
                "traits": ["intense", "fierce", "aggressive"],
                "weaknesses": ["angry", "hostile"],
                "catchphrases": ["I'm coming for you", "You're going down"],
                "historical_shame": ["Threatened to quit the league after losing to the last place team"]
            },
            "MickyMayn": {
                "traits": ["cheerful", "optimistic", "positive"],
                "weaknesses": ["naive", "unrealistic"],
                "catchphrases": ["It's all good", "We'll get them next time"],
                "historical_shame": ["Congratulated the wrong person for winning the championship"]
            }
        }
    
    def generate_team_roast(self, team_data: Dict, weekly_data: Dict, context: str = "general") -> str:
        """Generate a contextual roast for a team"""
        team_name = team_data.get('team', 'Unknown Team')
        owner_name = team_data.get('owner', 'Unknown Owner')
        rank = team_data.get('rank', 16)
        record = team_data.get('record', '0-0')
        points_for = team_data.get('points_for', 0)
        points_against = team_data.get('points_against', 0)
        
        # Get team personality
        personality = self.team_personalities.get(team_name, {})
        
        # Determine roast category based on performance
        roast_category = self._determine_roast_category(rank, record, points_for, points_against)
        
        # Generate contextual roast
        roast = self._generate_contextual_roast(
            team_name, owner_name, personality, roast_category, 
            team_data, weekly_data, context
        )
        
        # Save to history to avoid repetition
        self.roast_history[team_name].append(roast)
        self._save_roast_history()
        
        return roast
    
    def _determine_roast_category(self, rank: int, record: str, points_for: float, points_against: float) -> str:
        """Determine the appropriate roast category based on performance"""
        if rank <= 4:
            return "contender"
        elif rank <= 8:
            return "bubble"
        elif rank <= 12:
            return "pretender"
        else:
            return "basement"
    
    def _generate_contextual_roast(self, team_name: str, owner_name: str, personality: Dict, 
                                 category: str, team_data: Dict, weekly_data: Dict, context: str) -> str:
        """Generate a contextual roast based on team performance and personality"""
        
        # Base roasts by category
        base_roasts = {
            "contender": [
                "Sitting pretty at the top, but can you handle the pressure?",
                "Leading the league while playing the easiest schedule - impressive or lucky?",
                "Great record, but playoff time is when boys become men.",
                "The target is on your back now. How does it feel?",
                "First place is nice, but can you finish what you started?"
            ],
            "bubble": [
                "Fighting for that last playoff spot like it's Black Friday.",
                "One week you're hot, next week you're not. Make up your mind!",
                "Playoff hopes hanging by a thread thinner than your roster depth.",
                "The definition of mediocre - not good enough to be great, not bad enough to be memorable.",
                "Consistently inconsistent. At least you're consistent about something."
            ],
            "pretender": [
                "A win is a win, but that score won't cut it most weeks.",
                "Benefitted from playing the worst team in the league. A flattering record.",
                "Alarm bells ringing - this team is in trouble.",
                "The wheels are falling off faster than a NASCAR crash.",
                "Started strong, now you're just hoping for a miracle."
            ],
            "basement": [
                "Started the season right where you left off. In the bin.",
                "A shocking performance from a supposed contender. Awful start.",
                "The worst team in the league. A truly pathetic display.",
                "At this point, you're just playing for pride. And you're not even doing that well.",
                "The only thing you're leading in is disappointment."
            ]
        }
        
        # Get base roast
        base_roast = random.choice(base_roasts[category])
        
        # Add personality-specific elements
        personality_roast = self._add_personality_elements(base_roast, personality, team_name, owner_name)
        
        # Add contextual elements
        contextual_roast = self._add_contextual_elements(personality_roast, team_data, weekly_data, context)
        
        # Add historical shame if available
        if personality.get('historical_shame') and random.random() < 0.3:
            shame = random.choice(personality['historical_shame'])
            contextual_roast += f" Remember when {shame}? Yeah, we do too."
        
        return contextual_roast
    
    def _add_personality_elements(self, roast: str, personality: Dict, team_name: str, owner_name: str) -> str:
        """Add personality-specific elements to the roast"""
        if not personality:
            return roast
        
        traits = personality.get('traits', [])
        weaknesses = personality.get('weaknesses', [])
        catchphrases = personality.get('catchphrases', [])
        
        # Add trait-based roasts
        if 'confident' in traits and random.random() < 0.4:
            roast = roast.replace("you", f"you, {owner_name}")
            roast += " Your confidence is admirable, but misplaced."
        
        if 'overthinking' in weaknesses and random.random() < 0.3:
            roast += " Maybe stop overthinking every decision and just play the game."
        
        if 'arrogant' in weaknesses and random.random() < 0.3:
            roast += " Time to check that ego at the door."
        
        if 'lucky' in traits and random.random() < 0.3:
            roast += " Your luck is bound to run out eventually."
        
        # Add catchphrase references
        if catchphrases and random.random() < 0.2:
            catchphrase = random.choice(catchphrases)
            roast += f" '{catchphrase}' - sure, {owner_name}, sure."
        
        return roast
    
    def _add_contextual_elements(self, roast: str, team_data: Dict, weekly_data: Dict, context: str) -> str:
        """Add contextual elements based on current performance"""
        rank = team_data.get('rank', 16)
        record = team_data.get('record', '0-0')
        points_for = team_data.get('points_for', 0)
        points_against = team_data.get('points_against', 0)
        
        # Add record-based context
        if record and record != '0-0':
            try:
                # Handle different record formats (e.g., "2-0-0" or "2-0")
                record_parts = record.split('-')
                if len(record_parts) >= 2:
                    wins = int(record_parts[0])
                    losses = int(record_parts[1])
                else:
                    wins, losses = 0, 0
            except (ValueError, IndexError):
                wins, losses = 0, 0
            
            if wins == 0 and losses > 0:
                roast += f" {losses} losses and counting. At least you're consistent."
            elif losses == 0 and wins > 0:
                roast += f" {wins} wins so far, but the real test is yet to come."
            elif wins == losses:
                roast += f" Perfectly mediocre at {record}. The definition of average."
        
        # Add points-based context
        if points_for > 0:
            if points_for < 100:
                roast += f" {points_for} points? That's not going to cut it."
            elif points_for > 150:
                roast += f" {points_for} points is nice, but can you do it consistently?"
        
        # Add rank-based context
        if rank <= 4:
            roast += f" Ranked #{rank} now, but the pressure is mounting."
        elif rank >= 13:
            roast += f" Ranked #{rank} out of 16. At least you're not last... yet."
        
        return roast
    
    def generate_league_roast(self, weekly_data: Dict) -> str:
        """Generate a roast for the entire league"""
        standings = weekly_data.get('standings', [])
        if not standings:
            return "The league is so bad, even the roasts are struggling."
        
        # Find interesting stats
        highest_scorer = max(standings, key=lambda x: x.get('points_for', 0))
        lowest_scorer = min(standings, key=lambda x: x.get('points_for', 0))
        
        # Get points safely
        highest_points = highest_scorer.get('points_for', 0)
        lowest_points = lowest_scorer.get('points_for', 0)
        highest_team = highest_scorer.get('team', 'Unknown Team')
        lowest_team = lowest_scorer.get('team', 'Unknown Team')
        
        league_roasts = [
            f"This week, {highest_team} scored {highest_points:.1f} points while {lowest_team} managed {lowest_points:.1f}. The gap between first and last is wider than the Grand Canyon.",
            f"16 teams, 16 different levels of disappointment. At least you're all consistent in that regard.",
            f"The league is so competitive that the difference between first and last place is just a few bad decisions.",
            f"Another week, another reminder that fantasy football is 90% luck and 10% skill. Unfortunately, most of you are in the 90%.",
            f"The standings are so tight that one good week could change everything. Or one bad week could ruin everything. No pressure."
        ]
        
        return random.choice(league_roasts)
    
    def generate_matchup_roast(self, matchup: Dict) -> str:
        """Generate a roast for a specific matchup"""
        team1 = matchup['team1']
        team2 = matchup['team2']
        score1 = matchup['team1_score']
        score2 = matchup['team2_score']
        winner = matchup['winner']
        
        # Determine the intensity of the roast based on score difference
        score_diff = abs(score1 - score2)
        
        if score_diff < 5:
            return f"{team1} vs {team2} was decided by {score_diff:.1f} points. A nail-biter that probably gave both owners heart attacks."
        elif score_diff < 15:
            return f"{team1} vs {team2} was a {score_diff:.1f} point difference. {winner} won, but it wasn't exactly a blowout."
        else:
            return f"{team1} vs {team2} was a {score_diff:.1f} point beatdown. {winner} dominated, and the other team should probably just quit now."
    
    def generate_transaction_roast(self, transaction: Dict, transaction_type: str) -> str:
        """Generate a roast for a transaction"""
        if transaction_type == "trade":
            team = transaction.get('team', 'Unknown Team')
            owner = transaction.get('owner', 'Unknown Owner')
            description = transaction.get('description', 'No description available')
            
            trade_roasts = [
                f"{owner} ({team}) made a trade: {description}",
                f"Another trade in the league. {owner} ({team}) is making moves: {description}",
                f"The trade by {owner} ({team}) is either brilliant or disastrous. Time will tell: {description}"
            ]
            
            return random.choice(trade_roasts)
        
        elif transaction_type == "waiver":
            team = transaction.get('team', '')
            player = transaction.get('player', '')
            faab = transaction.get('faab_spent', 0)
            
            waiver_roasts = [
                f"{team} picked up {player} off waivers for {faab} FAAB. Desperate times call for desperate measures.",
                f"{team} spent {faab} FAAB on {player}. That's either a steal or a waste of money.",
                f"{team} added {player} to their roster. Let's see if this pickup pays off or if they'll regret it."
            ]
            
            return random.choice(waiver_roasts)
        
        return "A transaction happened. Exciting stuff."

def main():
    """Test the roasting engine"""
    engine = RoastingEngine()
    
    # Test data
    test_team = {
        "team": "JewTeam",
        "owner": "Jewish Lightning",
        "rank": 1,
        "record": "8-1",
        "points_for": 1234.5,
        "points_against": 1089.2
    }
    
    test_weekly_data = {
        "week": 1,
        "standings": [test_team],
        "matchups": [
            {
                "team1": "JewTeam",
                "team2": "gunga36",
                "team1_score": 120.5,
                "team2_score": 98.3,
                "winner": "JewTeam"
            }
        ]
    }
    
    # Generate roasts
    print("🔥 Roasting Engine Test 🔥")
    print("=" * 40)
    
    team_roast = engine.generate_team_roast(test_team, test_weekly_data)
    print(f"Team Roast: {team_roast}")
    
    league_roast = engine.generate_league_roast(test_weekly_data)
    print(f"League Roast: {league_roast}")
    
    matchup_roast = engine.generate_matchup_roast(test_weekly_data['matchups'][0])
    print(f"Matchup Roast: {matchup_roast}")

if __name__ == "__main__":
    main()
