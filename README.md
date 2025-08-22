# 🏆 16 Fantasies 1 Cup - Automated Fantasy Football Newsletter

A complete automated system for generating weekly fantasy football newsletters with team analysis, roasting content, and interactive features.

## 🌟 Features

### 📊 **Automated Data Processing**
- Kaggle integration for weekly data fetching
- Automatic standings and performance calculations
- Trade and waiver wire analysis
- Historical data tracking

### 📰 **Dynamic Newsletter Generation**
- Weekly HTML newsletters with custom themes
- Automated roasting content based on performance
- Interactive polls and comment sections
- PDF export functionality

### 👥 **Individual Team Profiles**
- Detailed analysis for each of 16 team owners
- Historical performance tracking
- Draft analysis and trade history
- Custom roasting sections

### 🚀 **Full Automation**
- GitHub Actions for scheduled updates
- Manual approval system for quality control
- Automatic Netlify deployment
- One-click newsletter publishing

## 🛠️ Setup Instructions

### 1. **Repository Setup**

```bash
# Clone or initialize your repository
git init
git add .
git commit -m "Initial setup"
git remote add origin https://github.com/your-username/16fantasies1cup.git
git push -u origin main
```

### 2. **Data Configuration**

Update the sample data files with your league information:

- `data/season-stats.json` - Current season overview
- `data/teams/*.json` - Individual team profiles (create one for each owner)
- `weeks.js` - Newsletter index

### 3. **Python Dependencies**

Install required packages:

```bash
pip install pandas requests kaggle jinja2
```

### 4. **Kaggle API Setup**

1. Go to [Kaggle.com](https://kaggle.com) → Account → API → Create New API Token
2. Download `kaggle.json` file
3. Set environment variables:
   ```bash
   export KAGGLE_USERNAME="your-username"
   export KAGGLE_KEY="your-api-key"
   ```

### 5. **GitHub Secrets Configuration**

Add these secrets to your GitHub repository (Settings → Secrets and variables → Actions):

```
KAGGLE_USERNAME=your_kaggle_username
KAGGLE_KEY=your_kaggle_api_key
NETLIFY_SITE_ID=your_netlify_site_id
NETLIFY_AUTH_TOKEN=your_netlify_token
```

### 6. **Netlify Setup**

1. Create account at [Netlify.com](https://netlify.com)
2. Connect your GitHub repository
3. Get your Site ID from Site Settings → General → Site information
4. Generate Personal Access Token from User Settings → Applications

### 7. **GitHub Actions Environment**

Create a GitHub Environment for manual approvals:
1. Go to Settings → Environments
2. Create environment named `production-approval`
3. Add required reviewers (yourself)
4. Enable "Required reviewers" protection rule

## 📅 Usage

### **Automatic Weekly Updates**

The system automatically runs every Tuesday at 8 AM EST after Monday Night Football:

1. **Data Fetching**: Pulls latest stats from your Kaggle notebook
2. **Newsletter Generation**: Creates HTML newsletter with roasting content
3. **Preview Creation**: Generates preview branch for review
4. **Manual Approval**: Waits for your approval (unless auto-deploy enabled)
5. **Deployment**: Publishes to Netlify and merges to main branch

### **Manual Updates**

Trigger updates manually via GitHub Actions:

1. Go to Actions → Weekly Fantasy Football Update
2. Click "Run workflow"
3. Enter week number and optional custom title
4. Choose whether to deploy immediately or wait for approval

### **Local Testing**

Test scripts locally:

```bash
# Fetch data for specific week
python scripts/fetch_kaggle_data.py --week 10

# Generate newsletter
python scripts/generate_newsletter.py --week 10 --title "Playoff Push"
```

## 📁 File Structure

```
16Fantasies1Cup/
├── 📄 index.html              # Main page with dashboard
├── 📄 week-*.html             # Generated newsletters
├── 📄 weeks.js                # Newsletter index
├── 🎨 Images/                 # League logos and assets
├── 👥 teams/
│   ├── 📄 index.html          # Team directory
│   └── 📄 *.html              # Individual team pages
├── 📊 data/
│   ├── 📄 season-stats.json   # Current season data
│   ├── 👥 teams/              # Individual team data
│   ├── 📈 historical/         # Multi-season data
│   └── 📅 weekly/             # Week-by-week data
├── 🤖 scripts/
│   ├── 📄 fetch_kaggle_data.py    # Data fetching
│   └── 📄 generate_newsletter.py  # Newsletter creation
└── 🔧 .github/workflows/
    └── 📄 weekly-update.yml   # Automation workflow
```

## 🎨 Customization

### **Team Profiles**

Edit team JSON files in `data/teams/` to customize:
- Team information and owner details
- Historical performance data
- Roasting material and signature moves
- Head-to-head records

### **Newsletter Content**

Modify `scripts/generate_newsletter.py` to customize:
- Roasting algorithms and content
- Section layouts and styling
- Poll questions and options
- Matchup analysis logic

### **Visual Design**

Update styling in HTML files:
- Color scheme (CSS variables in `:root`)
- Typography and fonts
- Layout and spacing
- Interactive elements

## 🔥 Roasting System

The automated roasting system generates content based on:

### **Performance Metrics**
- Weekly scores vs. league average
- Consistency ratings
- Playoff odds and power rankings
- Strength of schedule analysis

### **Historical Context**
- Previous season performance
- Draft pick success/failure rates
- Trade win/loss analysis
- Playoff history and clutch factor

### **Behavioral Patterns**
- Risk tolerance in drafts
- Waiver wire activity
- Trade frequency and strategy
- Lineup optimization skills

## 🚀 Deployment Options

### **Netlify (Recommended)**
- Free hosting for static sites
- Automatic deploys from GitHub
- Custom domain support
- Built-in form handling

### **Alternative Platforms**
- **GitHub Pages**: Free, simple setup
- **Vercel**: Fast, modern platform
- **Firebase Hosting**: Google's hosting solution

## 🛠️ Troubleshooting

### **Common Issues**

1. **Kaggle API Errors**
   - Verify credentials in GitHub secrets
   - Check Kaggle dataset permissions
   - Ensure API token hasn't expired

2. **Netlify Deployment Failures**
   - Confirm site ID and auth token
   - Check build settings and environment variables
   - Review deployment logs

3. **Data Processing Errors**
   - Validate JSON file formats
   - Check for missing required fields
   - Verify data types and structures

4. **GitHub Actions Failures**
   - Review workflow logs for specific errors
   - Check secret configurations
   - Ensure required permissions are set

### **Getting Help**

- Check the [Issues](https://github.com/your-username/16fantasies1cup/issues) page
- Review GitHub Actions logs for detailed error messages
- Test scripts locally before pushing changes

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Feel free to submit issues and enhancement requests! Pull requests are welcome.

---

**Built with ❤️ for fantasy football trash talk and maximum league engagement** 🏈🔥