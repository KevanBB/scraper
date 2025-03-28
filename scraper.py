import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re
import os
from urllib.parse import urlparse
import time

class RecuMeScraper:
    def __init__(self):
        self.base_url = "https://recu.me"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.download_path = "downloads"
        self._create_download_directory()

    def _create_download_directory(self):
        """Create downloads directory if it doesn't exist"""
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)

    def _extract_video_url(self, soup):
        """Extract the video URL from the page"""
        try:
            # Look for the video source in the page
            video_elem = soup.find('video')
            if video_elem and video_elem.get('src'):
                return video_elem['src']
            
            # Look for video source in script tags
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string and 'videoUrl' in script.string:
                    # Extract URL from script content
                    url_match = re.search(r'videoUrl\s*=\s*[\'"]([^\'"]+)[\'"]', script.string)
                    if url_match:
                        return url_match.group(1)
            
            return None
        except Exception as e:
            print(f"Error extracting video URL: {str(e)}")
            return None

    def scrape_url(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract video information
            video_info = {}
            
            # Get performer name
            performer_elem = soup.find('a', class_='performer')
            if performer_elem:
                video_info['performer'] = performer_elem.text.strip()
            
            # Get video title and metadata
            title_elem = soup.find('div', class_='title')
            if title_elem:
                video_info['title'] = title_elem.text.strip()
            
            # Get video details
            video_info_sub = soup.find('div', class_='video-info-sub')
            if video_info_sub:
                # Extract views
                views_elem = video_info_sub.find('span', class_='video-views')
                if views_elem:
                    views_text = views_elem.text.strip()
                    video_info['views'] = int(re.search(r'\d+', views_text).group())
                
                # Extract date and time
                date_elem = video_info_sub.find('i', class_='fa-regular fa-calendar')
                if date_elem:
                    date_text = date_elem.find_next(text=True).strip()
                    video_info['date'] = date_text
                
                # Extract duration
                duration_elem = video_info_sub.find('i', class_='fa-regular fa-clock')
                if duration_elem:
                    duration_text = duration_elem.find_next(text=True).strip()
                    video_info['duration'] = duration_text
                
                # Extract likes percentage
                likes_elem = video_info_sub.find('span', id='likes_percent')
                if likes_elem:
                    video_info['likes_percentage'] = likes_elem.text.strip()
                
                # Extract bookmarks count
                bookmarks_elem = video_info_sub.find('span', class_='video-bookmark-counter')
                if bookmarks_elem:
                    video_info['bookmarks'] = int(bookmarks_elem.text.strip())
            
            # Get video thumbnail
            thumb_elem = soup.find('img', id=lambda x: x and x.startswith('thumb_'))
            if thumb_elem and 'style' in thumb_elem.attrs:
                style = thumb_elem['style']
                thumbnail_url = re.search(r"url\('([^']+)'\)", style)
                if thumbnail_url:
                    video_info['thumbnail_url'] = thumbnail_url.group(1)
            
            # Get video ID from URL
            video_id_match = re.search(r'/video/(\d+)/', url)
            if video_id_match:
                video_info['video_id'] = video_id_match.group(1)
            
            # Extract video URL
            video_url = self._extract_video_url(soup)
            if video_url:
                video_info['video_url'] = video_url
            
            # Add metadata
            video_info['timestamp'] = datetime.now().isoformat()
            video_info['url'] = url
            
            return video_info
            
        except Exception as e:
            return {'error': str(e)}

    def download_video(self, video_info, progress_callback=None):
        """
        Download the video file
        Args:
            video_info: Dictionary containing video information including video_url
            progress_callback: Optional callback function to report download progress
        Returns:
            dict: Information about the download result
        """
        try:
            if 'video_url' not in video_info:
                return {'error': 'No video URL found in video info'}

            # Create filename from performer and date
            performer = video_info.get('performer', 'unknown')
            date = video_info.get('date', datetime.now().strftime('%Y%m%d'))
            date = re.sub(r'[^\d]', '', date)  # Remove non-digits from date
            filename = f"{performer}_{date}.mp4"
            filepath = os.path.join(self.download_path, filename)

            # Download the video
            response = requests.get(video_info['video_url'], headers=self.headers, stream=True)
            response.raise_for_status()
            
            # Get total file size
            total_size = int(response.headers.get('content-length', 0))
            block_size = 8192  # 8 KB chunks
            downloaded = 0

            with open(filepath, 'wb') as f:
                for data in response.iter_content(block_size):
                    downloaded += len(data)
                    f.write(data)
                    if progress_callback:
                        progress = (downloaded / total_size) * 100
                        progress_callback(progress)

            return {
                'success': True,
                'filepath': filepath,
                'filename': filename,
                'size': total_size
            }

        except Exception as e:
            return {'error': str(e)}

    def save_to_file(self, data, filename='scraped_data.json'):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            return False 