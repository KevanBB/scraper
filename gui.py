import customtkinter as ctk
from scraper import RecuMeScraper
import json
from datetime import datetime
import os
import threading

class ScraperGUI:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Recu.me Scraper")
        self.window.geometry("800x600")
        
        # Configure grid
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=1)
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # URL input
        self.url_label = ctk.CTkLabel(self.main_frame, text="Enter URL to scrape:")
        self.url_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.url_entry = ctk.CTkEntry(self.main_frame, width=400)
        self.url_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        
        # Buttons frame
        self.buttons_frame = ctk.CTkFrame(self.main_frame)
        self.buttons_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        
        # Scrape button
        self.scrape_button = ctk.CTkButton(
            self.buttons_frame, 
            text="Scrape Data",
            command=self.scrape_data
        )
        self.scrape_button.pack(side="left", padx=5)
        
        # Download button
        self.download_button = ctk.CTkButton(
            self.buttons_frame,
            text="Download Video",
            command=self.download_video,
            state="disabled"
        )
        self.download_button.pack(side="left", padx=5)
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.main_frame)
        self.progress_bar.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        self.progress_bar.set(0)
        
        # Progress label
        self.progress_label = ctk.CTkLabel(self.main_frame, text="")
        self.progress_label.grid(row=4, column=0, padx=10, pady=5)
        
        # Results text area
        self.results_text = ctk.CTkTextbox(self.main_frame, height=300)
        self.results_text.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")
        
        # Status label
        self.status_label = ctk.CTkLabel(self.main_frame, text="")
        self.status_label.grid(row=6, column=0, padx=10, pady=5)
        
        self.scraper = RecuMeScraper()
        self.current_video_info = None
        
    def update_progress(self, progress):
        """Update the progress bar and label"""
        self.progress_bar.set(progress / 100)
        self.progress_label.configure(text=f"Downloading: {progress:.1f}%")
        self.window.update()
        
    def scrape_data(self):
        url = self.url_entry.get()
        if not url:
            self.status_label.configure(text="Please enter a URL")
            return
            
        self.status_label.configure(text="Scraping in progress...")
        self.window.update()
        
        try:
            self.current_video_info = self.scraper.scrape_url(url)
            
            if 'error' in self.current_video_info:
                self.status_label.configure(text=f"Error: {self.current_video_info['error']}")
                self.download_button.configure(state="disabled")
                return
                
            # Save data to file
            filename = f"scraped_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            if self.scraper.save_to_file(self.current_video_info, filename):
                self.status_label.configure(text=f"Data saved to {filename}")
            else:
                self.status_label.configure(text="Error saving data")
                
            # Display results
            self.results_text.delete("1.0", "end")
            self.results_text.insert("1.0", json.dumps(self.current_video_info, indent=4))
            
            # Enable download button if video URL is available
            if 'video_url' in self.current_video_info:
                self.download_button.configure(state="normal")
            else:
                self.download_button.configure(state="disabled")
            
        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}")
            self.download_button.configure(state="disabled")
            
    def download_video(self):
        if not self.current_video_info:
            self.status_label.configure(text="No video data available")
            return
            
        # Disable buttons during download
        self.scrape_button.configure(state="disabled")
        self.download_button.configure(state="disabled")
        self.progress_bar.set(0)
        self.progress_label.configure(text="Starting download...")
        
        # Start download in a separate thread
        thread = threading.Thread(target=self._download_thread)
        thread.daemon = True
        thread.start()
        
    def _download_thread(self):
        try:
            result = self.scraper.download_video(self.current_video_info, self.update_progress)
            
            if 'error' in result:
                self.status_label.configure(text=f"Download error: {result['error']}")
            else:
                self.status_label.configure(text=f"Download complete: {result['filename']}")
                self.progress_label.configure(text="Download complete!")
                
        except Exception as e:
            self.status_label.configure(text=f"Download error: {str(e)}")
            
        finally:
            # Re-enable buttons
            self.scrape_button.configure(state="normal")
            if 'video_url' in self.current_video_info:
                self.download_button.configure(state="normal")
            
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = ScraperGUI()
    app.run() 