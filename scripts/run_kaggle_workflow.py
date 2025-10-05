#!/usr/bin/env python3
"""
Kaggle Workflow Automation Script
Helps you run the complete workflow from Kaggle notebook to newsletter
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Main workflow function"""
    print("🏈 Kaggle Newsletter Workflow")
    print("=" * 40)
    
    # Get week number from user
    try:
        week = int(input("Enter week number: "))
    except ValueError:
        print("❌ Please enter a valid week number")
        return
    
    print(f"\n📊 Processing Week {week}...")
    
    # Step 1: Check if YAML file exists
    yaml_file = f"creative_brief_week{week}.yaml"
    yaml_path = Path(f"data/weekly/{yaml_file}")
    
    if not yaml_path.exists():
        print(f"❌ YAML file not found: {yaml_path}")
        print("\n📋 To get the YAML file:")
        print("1. Run your Kaggle notebook")
        print("2. Download the creative_brief_week{week}.yaml file")
        print("3. Place it in data/weekly/")
        print("4. Run this script again")
        return
    
    print(f"✅ Found YAML file: {yaml_path}")
    
    # Step 2: Convert YAML to newsletter format
    print("\n🔄 Converting YAML data...")
    try:
        result = subprocess.run([
            sys.executable, "scripts/convert_kaggle_data.py",
            "--yaml-file", str(yaml_path),
            "--week", str(week)
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ YAML conversion successful")
        else:
            print(f"❌ YAML conversion failed: {result.stderr}")
            return
    except Exception as e:
        print(f"❌ Error converting YAML: {e}")
        return
    
    # Step 3: Generate post-week newsletter
    print("\n📰 Generating post-week newsletter...")
    try:
        result = subprocess.run([
            sys.executable, "scripts/generate_newsletter.py",
            "--week", str(week),
            "--title", f"Week {week} Recap"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Post-week newsletter generated")
        else:
            print(f"❌ Newsletter generation failed: {result.stderr}")
            return
    except Exception as e:
        print(f"❌ Error generating newsletter: {e}")
        return
    
    # Step 4: Generate pre-week newsletter for next week
    next_week = week + 1
    print(f"\n🔮 Generating pre-week newsletter for Week {next_week}...")
    try:
        result = subprocess.run([
            sys.executable, "scripts/generate_preweek_newsletter.py",
            "--week", str(next_week),
            "--title", f"Week {next_week} Preview"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Pre-week newsletter generated")
        else:
            print(f"❌ Pre-week newsletter generation failed: {result.stderr}")
    except Exception as e:
        print(f"❌ Error generating pre-week newsletter: {e}")
    
    # Step 5: Show results
    print("\n🎉 Workflow Complete!")
    print("=" * 40)
    print(f"📁 Generated files:")
    print(f"   - week-{week:02d}.html (Post-week newsletter)")
    print(f"   - preweek-{next_week:02d}.html (Pre-week newsletter)")
    print(f"   - data/weekly/week-{week:02d}.json (Processed data)")
    
    print(f"\n🌐 To view newsletters:")
    print(f"   - Open week-{week:02d}.html in your browser")
    print(f"   - Open preweek-{next_week:02d}.html in your browser")

if __name__ == "__main__":
    main()


