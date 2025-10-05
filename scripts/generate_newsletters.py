#!/usr/bin/env python3
"""
Unified Newsletter Generator
Generates both pre-week and post-week newsletters
"""

import argparse
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from scripts.generate_newsletter import NewsletterGenerator
from scripts.generate_preweek_newsletter import PreWeekNewsletterGenerator

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Generate fantasy football newsletters')
    parser.add_argument('--week', type=int, required=True, help='Week number')
    parser.add_argument('--type', choices=['pre', 'post', 'both'], default='post', 
                       help='Newsletter type: pre (preview), post (recap), or both')
    parser.add_argument('--title', help='Custom title for the newsletter')
    
    args = parser.parse_args()
    
    try:
        if args.type in ['pre', 'both']:
            print("🔮 Generating pre-week newsletter...")
            preweek_generator = PreWeekNewsletterGenerator()
            preweek_file = preweek_generator.generate_preweek_newsletter(args.week, args.title)
            print(f"✅ Pre-week newsletter: {preweek_file}")
        
        if args.type in ['post', 'both']:
            print("📰 Generating post-week newsletter...")
            postweek_generator = NewsletterGenerator()
            postweek_file = postweek_generator.generate_newsletter(args.week, args.title)
            print(f"✅ Post-week newsletter: {postweek_file}")
        
        print("🎉 Newsletter generation complete!")
        
    except Exception as e:
        print(f"❌ Error generating newsletters: {e}")
        raise

if __name__ == "__main__":
    main()

