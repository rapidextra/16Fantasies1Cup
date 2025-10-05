# 🏈 Upcoming Matchups Guide

This guide shows you how to get upcoming matchups for your pre-week newsletters.

## 🎯 **Three Methods to Get Upcoming Matchups**

### **Method 1: Sleeper API (Most Accurate)**
Get real upcoming matchups directly from Sleeper.

```bash
# Get upcoming matchups from Sleeper API
python scripts/get_upcoming_matchups.py --week 3 --method sleeper --league-id YOUR_LEAGUE_ID --save
```

**Requirements:**
- Your Sleeper league ID
- Internet connection
- Sleeper API access

**Benefits:**
- Real upcoming matchups
- Projected points
- Accurate team pairings
- Official league schedule

### **Method 2: Standings-Based (Fallback)**
Generate matchups based on current standings order.

```bash
# Generate matchups from current standings
python scripts/get_upcoming_matchups.py --week 3 --method standings --save
```

**Requirements:**
- Current standings data
- No internet needed

**Benefits:**
- Always works
- Uses your existing data
- Simple and reliable

### **Method 3: Historical Patterns (Advanced)**
Generate matchups based on historical scheduling patterns.

```bash
# Generate matchups from historical data
python scripts/get_upcoming_matchups.py --week 3 --method historical --save
```

**Requirements:**
- Historical matchup data
- More complex setup

**Benefits:**
- More realistic matchups
- Considers past scheduling

## 🚀 **Quick Start**

### **Step 1: Get Your Sleeper League ID**
1. Go to your Sleeper league
2. Look at the URL: `https://sleeper.app/leagues/YOUR_LEAGUE_ID`
3. Copy the league ID from the URL

### **Step 2: Test the API**
```bash
# Test with your league ID
python scripts/get_upcoming_matchups.py --week 3 --method sleeper --league-id 1234567890
```

### **Step 3: Save Matchups**
```bash
# Save matchups for pre-week newsletter
python scripts/get_upcoming_matchups.py --week 3 --method sleeper --league-id 1234567890 --save
```

### **Step 4: Generate Pre-Week Newsletter**
```bash
# Generate newsletter with upcoming matchups
python scripts/generate_simple_preweek_newsletter.py --week 3 --title "The Calm Before the Storm"
```

## 📊 **Data Structure**

### **Upcoming Matchups File**
```json
{
  "week": 3,
  "season": 2025,
  "generated_at": "2025-01-15T10:30:00",
  "matchups": [
    {
      "week": 3,
      "team1": {
        "owner": "healzyswarriors",
        "roster_id": 1,
        "points": 0,
        "projected_points": 95.5,
        "wins": 2,
        "losses": 0,
        "points_for": 216.64
      },
      "team2": {
        "owner": "FattyC26",
        "roster_id": 2,
        "points": 0,
        "projected_points": 88.2,
        "wins": 1,
        "losses": 1,
        "points_for": 185.32
      },
      "matchup_id": "week_3_matchup_1",
      "status": "upcoming"
    }
  ]
}
```

## 🔧 **Integration with Your Workflow**

### **Option 1: Manual Generation**
```bash
# Generate upcoming matchups
python scripts/get_upcoming_matchups.py --week 3 --method sleeper --league-id YOUR_LEAGUE_ID --save

# Generate pre-week newsletter
python scripts/generate_simple_preweek_newsletter.py --week 3 --title "The Calm Before the Storm"
```

### **Option 2: Automated Workflow**
Add to your existing automation:

```python
# In your main script
from scripts.get_upcoming_matchups import UpcomingMatchupsFetcher

# Get upcoming matchups
fetcher = UpcomingMatchupsFetcher("YOUR_LEAGUE_ID")
matchups = fetcher.get_upcoming_matchups(week_number, "sleeper")
fetcher.save_upcoming_matchups(week_number, matchups)

# Generate newsletter
generator = SimplePreWeekNewsletterGenerator()
generator.generate_preweek_newsletter(week_number)
```

### **Option 3: Kaggle Notebook Integration**
Add to your Kaggle notebook:

```python
# Add this to your notebook
import requests

def get_upcoming_matchups(league_id, week):
    url = f"https://api.sleeper.app/v1/league/{league_id}/matchups/{week}"
    response = requests.get(url)
    return response.json()

# Get upcoming matchups
upcoming_matchups = get_upcoming_matchups("YOUR_LEAGUE_ID", WEEK_TO_ANALYZE + 1)

# Add to your creative brief
creative_brief["UpcomingMatchups"] = upcoming_matchups
```

## 🎯 **Pre-Week Newsletter Features**

### **With Real Upcoming Matchups:**
- ✅ Actual team pairings
- ✅ Projected points
- ✅ Realistic storylines
- ✅ Accurate records

### **With Standings-Based Matchups:**
- ✅ Always works
- ✅ Uses current data
- ✅ Simple generation
- ✅ Fallback option

## 🚨 **Troubleshooting**

### **Sleeper API Issues**
```bash
# Test API connection
curl "https://api.sleeper.app/v1/league/YOUR_LEAGUE_ID/matchups/3"
```

### **No Matchups Found**
```bash
# Check if week exists
python scripts/get_upcoming_matchups.py --week 3 --method standings --save
```

### **Permission Errors**
```bash
# Check file permissions
ls -la data/weekly/
```

## 📈 **Best Practices**

1. **Always use Sleeper API when possible** - Most accurate
2. **Have a fallback method** - Standings-based works as backup
3. **Save matchups to file** - Avoid repeated API calls
4. **Test with different weeks** - Ensure reliability
5. **Monitor API limits** - Don't overuse Sleeper API

## 🔄 **Automation Ideas**

### **GitHub Actions**
```yaml
# Add to your workflow
- name: Get Upcoming Matchups
  run: |
    python scripts/get_upcoming_matchups.py --week ${{ github.event.inputs.week }} --method sleeper --league-id ${{ secrets.SLEEPER_LEAGUE_ID }} --save
```

### **Cron Job**
```bash
# Run every Tuesday at 9 AM
0 9 * * 2 python scripts/get_upcoming_matchups.py --week $(date +%V) --method sleeper --league-id YOUR_LEAGUE_ID --save
```

### **Python Script**
```python
# Run before newsletter generation
import subprocess
subprocess.run(["python", "scripts/get_upcoming_matchups.py", "--week", str(week), "--method", "sleeper", "--league-id", league_id, "--save"])
```

## 🎉 **Success!**

You now have a complete system for getting upcoming matchups:

1. **Real matchups** from Sleeper API
2. **Fallback generation** from standings
3. **Automatic integration** with pre-week newsletters
4. **Flexible methods** for different scenarios

Your pre-week newsletters will now show actual upcoming matchups instead of just standings-based predictions!


