import argparse
from scraper import RecuMeScraper
import json
from datetime import datetime
import sys
import time
import getpass

def print_progress(progress):
    """Print download progress to the terminal"""
    sys.stdout.write(f"\rDownloading: {progress:.1f}%")
    sys.stdout.flush()

def main():
    parser = argparse.ArgumentParser(description='Recu.me Video Scraper')
    parser.add_argument('url', help='URL of the video to scrape')
    parser.add_argument('--download', '-d', action='store_true', help='Download the video after scraping')
    parser.add_argument('--output', '-o', help='Output JSON file for scraped data (default: scraped_data_TIMESTAMP.json)')
    parser.add_argument('--username', '-u', help='Your recu.me username')
    parser.add_argument('--password', '-p', help='Your recu.me password (not recommended, will prompt if not provided)')
    args = parser.parse_args()

    scraper = RecuMeScraper()
    
    # Handle login
    if not args.username:
        args.username = input("Enter your recu.me username: ")
    
    if not args.password:
        args.password = getpass.getpass("Enter your recu.me password: ")
    
    print("\nLogging in...")
    if not scraper.login(args.username, args.password):
        print("Login failed. Please check your credentials.")
        sys.exit(1)
    print("Login successful!")
    
    print(f"\nScraping URL: {args.url}")
    video_info = scraper.scrape_url(args.url)
    
    if 'error' in video_info:
        print(f"Error: {video_info['error']}")
        sys.exit(1)
    
    # Save scraped data
    if not args.output:
        args.output = f"scraped_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    if scraper.save_to_file(video_info, args.output):
        print(f"\nScraped data saved to: {args.output}")
    else:
        print("\nError saving scraped data")
        sys.exit(1)
    
    # Print scraped information
    print("\nScraped Information:")
    print("-" * 50)
    print(f"Performer: {video_info.get('performer', 'N/A')}")
    print(f"Title: {video_info.get('title', 'N/A')}")
    print(f"Date: {video_info.get('date', 'N/A')}")
    print(f"Duration: {video_info.get('duration', 'N/A')}")
    print(f"Views: {video_info.get('views', 'N/A')}")
    print(f"Likes: {video_info.get('likes_percentage', 'N/A')}")
    print(f"Bookmarks: {video_info.get('bookmarks', 'N/A')}")
    print("-" * 50)
    
    # Download video if requested
    if args.download:
        if 'video_url' not in video_info:
            print("\nError: No video URL found")
            sys.exit(1)
            
        print("\nStarting video download...")
        result = scraper.download_video(video_info, print_progress)
        
        if 'error' in result:
            print(f"\nDownload error: {result['error']}")
            sys.exit(1)
        else:
            print(f"\nDownload complete: {result['filename']}")
            print(f"File saved to: {result['filepath']}")
            print(f"File size: {result['size'] / (1024*1024):.2f} MB")

if __name__ == "__main__":
    main() 