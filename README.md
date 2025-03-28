# Recu.me Scraper

A command-line tool for scraping and downloading videos from recu.me.

## Features

- Scrape video metadata and information
- Download videos with progress tracking
- Save scraped data to JSON files
- Command-line interface for easy use
- Secure login handling

## Requirements

- Python 3.7 or higher
- Required packages listed in `requirements.txt`
- A recu.me account

## Installation

1. Clone this repository
2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

To scrape video information without downloading (will prompt for login):
```bash
python cli.py "https://recu.me/[performer]/video/[video_id]/play"
```

### Download Video

To scrape and download the video (will prompt for login):
```bash
python cli.py "https://recu.me/[performer]/video/[video_id]/play" --download
```

### Specify Output File

To save scraped data to a specific JSON file (will prompt for login):
```bash
python cli.py "https://recu.me/[performer]/video/[video_id]/play" --output "my_data.json"
```

### Login Options

You can provide your login credentials in several ways:

1. Interactive prompt (recommended):
```bash
python cli.py "https://recu.me/[performer]/video/[video_id]/play"
```

2. Command line arguments (not recommended for password):
```bash
python cli.py "https://recu.me/[performer]/video/[video_id]/play" --username "your_username" --password "your_password"
```

3. Username only (will prompt for password):
```bash
python cli.py "https://recu.me/[performer]/video/[video_id]/play" --username "your_username"
```

### All Options

```bash
python cli.py --help
```

## Data Storage

- Scraped data is saved to JSON files
- Downloaded videos are saved in the `downloads` directory
- Video files are named in the format: `performer_YYYYMMDD.mp4`

## Note

Make sure to respect the website's robots.txt and terms of service when scraping data. 