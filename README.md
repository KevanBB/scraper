# Recu.me Scraper

A user-friendly GUI application for scraping data from recu.me websites.

## Features

- Modern, user-friendly interface
- Easy URL input and data scraping
- Automatic data saving to JSON files
- Real-time status updates
- Error handling and user feedback

## Requirements

- Python 3.7 or higher
- Required packages listed in `requirements.txt`

## Installation

1. Clone this repository to your VPS
2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the GUI application:
```bash
python gui.py
```

2. Enter the URL you want to scrape in the input field
3. Click "Scrape Data" to start the scraping process
4. The scraped data will be displayed in the text area and saved to a JSON file

## Data Storage

Scraped data is automatically saved to JSON files in the following format:
- Filename: `scraped_data_YYYYMMDD_HHMMSS.json`
- Each file contains the scraped data with timestamp and URL information

## Note

Make sure to respect the website's robots.txt and terms of service when scraping data. 