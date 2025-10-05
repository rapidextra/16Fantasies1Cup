# 🏈 Kaggle Notebook Integration Guide

This guide explains how to integrate your Kaggle notebook with the newsletter system.

## 📋 Overview

Your Kaggle notebook generates comprehensive fantasy football analysis and exports it as YAML creative briefs. The newsletter system automatically converts these YAML files into beautiful HTML newsletters.

## 🔄 Data Flow

```
Kaggle Notebook → YAML Creative Brief → Newsletter System → HTML Newsletter
```

## 📊 Your Notebook Features

### **Data Sources**
- **Sleeper API**: Fetches real-time fantasy football data
- **Multi-Season Support**: 2023, 2024, 2025 seasons
- **League IDs**: Automatically configured for each season

### **Analysis Capabilities**
- **Standings Calculation**: Overall and divisional rankings
- **Matchup Analysis**: Detailed team performance breakdowns
- **Player Performance**: Individual player scores and optimal lineups
- **Advanced Metrics**: Coach ratings, luck ratings, key mistakes
- **Weekly Awards**: 5 different award categories

### **Output Format**
- **YAML Creative Brief**: `creative_brief_weekX.yaml`
- **Comprehensive Data**: All analysis results in structured format
- **Ready for Newsletter**: Directly compatible with newsletter system

## 🛠️ Integration Steps

### **1. Configure Your Dataset**
Update `config.py` with your Kaggle dataset:
```python
KAGGLE_DATASET = "jgade/16-fantasies-1-cup"
```

### **2. Set Up Kaggle API**
```bash
pip install kaggle
export KAGGLE_USERNAME="your-username"
export KAGGLE_KEY="your-api-key"
```

### **3. Run Your Notebook**
1. Execute your Kaggle notebook for the desired week
2. Ensure it generates `creative_brief_weekX.yaml`
3. Upload the YAML file to your Kaggle dataset

### **4. Generate Newsletter**
```bash
# The system will automatically fetch from Kaggle
python scripts/fetch_kaggle_data.py --week 2
python scripts/generate_newsletter.py --week 2
```

## 📁 Expected YAML Structure

Your notebook should generate YAML files with this structure:

```yaml
WeekInfo:
  Season: 2025
  Week: 2

Standings:
  Overall:
    - Owner: healzyswarriors
      Division: BTK
      Wins: 2
      Losses: 0
      Ties: 0
      PF: 216.64
      PA: 184.32
      OverallRank: 1
  Divisional:
    BTK: [...]
    FLO: [...]

Matchups:
  - MatchupID: 1
    Teams:
      - Owner: gunga36
        Division: BTK
        Score: 83.28
        Starters: [...]
        Bench: [...]
        MVP: {...}
        Bust: {...}
        CoachRating: 69.67
        LuckRating: -3.41
        KeyMistake: "..."

Awards:
  HighestScorer:
    Owner: Wicka
    Score: 125.56
  CoachOfTheWeek:
    Owner: Stampy
    CoachRating: "100.0% lineup efficiency"
  BoneheadOfTheWeek:
    Owner: gunga36
    KeyMistake: "..."
    BenchPointsLost: 36.26
    LossMargin: 16.72
  Luckiest:
    Owner: coopersallstarz
    Score: 73.38
    Description: "Would have lost to 10 of 15 teams, but still won"
  Unluckiest:
    Owner: Poddy
    Score: 99.24
    Description: "Would have beaten 10 of 15 teams, but still lost"
```

## 🎯 Newsletter Features

### **Post-Week Newsletters**
- **Real Standings**: Uses your actual league standings
- **Matchup Analysis**: Detailed breakdowns with real scores
- **Awards Section**: Highlights your calculated awards
- **Enhanced Roasting**: Contextual roasts based on real performance
- **Transaction Analysis**: Generated from actual team performance

### **Pre-Week Newsletters**
- **Current Standings**: Shows latest available standings
- **Predictions**: Smart predictions for upcoming week
- **Storylines**: Dynamic narratives based on current performance
- **Waiver Wire**: Recommendations based on team needs
- **Weather Watch**: Weather impact analysis

## 🔧 Troubleshooting

### **Common Issues**

1. **YAML File Not Found**
   - Ensure your notebook generates the correct filename format
   - Check that the file is uploaded to your Kaggle dataset

2. **Data Format Mismatch**
   - Verify your YAML structure matches the expected format
   - Check that all required fields are present

3. **Team Name Mapping**
   - Update `config.py` with correct owner-to-team mappings
   - Ensure owner names match between notebook and config

### **Testing Integration**

```bash
# Test with mock data first
python scripts/fetch_kaggle_data.py --week 2

# Test newsletter generation
python scripts/generate_newsletter.py --week 2

# Test pre-week newsletter
python scripts/generate_preweek_newsletter.py --week 3
```

## 📈 Advanced Features

### **Custom Analysis**
Your notebook can include additional analysis that will be automatically integrated:
- **Player Projections**: Future performance predictions
- **Trade Analysis**: Trade impact calculations
- **Injury Reports**: Player injury status and impact
- **Weather Analysis**: Weather impact on games

### **Automated Workflow**
1. **Monday**: Run your Kaggle notebook for completed week
2. **Tuesday**: Newsletter system automatically generates post-week newsletter
3. **Wednesday**: Generate pre-week newsletter for upcoming week
4. **Repeat**: Automated weekly cycle

## 🎉 Benefits

- **Real Data**: Uses actual fantasy football performance data
- **Comprehensive Analysis**: Leverages your advanced notebook analysis
- **Automated Generation**: Minimal manual intervention required
- **Professional Output**: Beautiful HTML newsletters with real insights
- **Scalable**: Works for any number of teams and weeks

Your Kaggle notebook provides the data foundation, and the newsletter system transforms it into engaging, professional newsletters for your league!


