import os
import yt_dlp
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import threading

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Downloader")
        self.root.geometry("600x400")
        self.setup_ui()
        self.downloading = False
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()

    def configure_styles(self):
        self.style.configure('TButton', font=('Arial', 10), padding=6)
        self.style.configure('TLabel', font=('Arial', 10))
        self.style.configure('TEntry', font=('Arial', 10), padding=5)
        self.style.configure('Header.TLabel', font=('Arial', 14, 'bold'))
        self.style.configure('Status.TLabel', font=('Arial', 9), foreground='gray')

    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        ttk.Label(main_frame, text="YouTube Downloader", style='Header.TLabel').grid(row=0, column=0, columnspan=3, pady=10)

        # URL Input
        ttk.Label(main_frame, text="YouTube URL:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.url_entry = ttk.Entry(main_frame, width=50)
        self.url_entry.grid(row=1, column=1, columnspan=2, sticky=tk.EW, pady=5)

        # Resolution Selection
        ttk.Label(main_frame, text="Resolution:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.resolution_var = tk.StringVar(value="1080")
        self.res_menu = ttk.Combobox(main_frame, textvariable=self.resolution_var, 
                                   values=["360", "480", "720", "1080", "1440", "2160"], state="readonly")
        self.res_menu.grid(row=2, column=1, sticky=tk.W, pady=5)

        # Download Folder
        ttk.Label(main_frame, text="Download Folder:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.output_folder = tk.StringVar(value=os.path.expanduser("~/Downloads"))
        ttk.Entry(main_frame, textvariable=self.output_folder, width=40).grid(row=3, column=1, sticky=tk.EW, pady=5)
        ttk.Button(main_frame, text="Browse", command=self.select_folder).grid(row=3, column=2, sticky=tk.W, pady=5)

        # Progress/Log
        self.log_area = ScrolledText(main_frame, height=8, wrap=tk.WORD, state='disabled')
        self.log_area.grid(row=4, column=0, columnspan=3, sticky=tk.NSEW, pady=10)

        # Download Button
        self.download_btn = ttk.Button(main_frame, text="Start Download", command=self.start_download)
        self.download_btn.grid(row=5, column=0, columnspan=3, pady=10)

        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)

    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.output_folder.set(folder_selected)

    def log_message(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def start_download(self):
        if self.downloading:
            return

        url = self.url_entry.get()
        res = self.resolution_var.get()
        output_path = self.output_folder.get()

        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        if not output_path:
            messagebox.showerror("Error", "Please select a download folder")
            return

        self.downloading = True
        self.download_btn.config(text="Downloading...", state=tk.DISABLED)
        self.log_message("Starting download...")

        # Start download in separate thread
        threading.Thread(target=self.perform_download, args=(url, output_path, res), daemon=True).start()

    def perform_download(self, url, output_path, resolution):
        try:
            ydl_opts = {
                'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                'format': f'bestvideo[height<={resolution}]+bestaudio/best',
                'progress_hooks': [self.progress_hook],
                'merge_output_format': 'mp4'
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                self.log_message(f"\nDownload complete: {info['title']}")

        except Exception as e:
            self.log_message(f"\nError: {str(e)}")
        finally:
            self.downloading = False
            self.root.after(0, self.download_complete)

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            progress = f"Downloading: {d.get('_percent_str', '')} | Speed: {d.get('_speed_str', '')}"
            self.root.after(0, self.log_message, progress)

    def download_complete(self):
        self.download_btn.config(text="Start Download", state=tk.NORMAL)
        messagebox.showinfo("Info", "Download completed!")

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()