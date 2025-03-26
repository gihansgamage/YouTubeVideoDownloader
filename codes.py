from pytube import YouTube, Playlist
import os

# def download_video(url, output_path):
#     try:
#         yt = YouTube(url)
#         stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()
#         print(f"Downloading: {yt.title} ({stream.resolution})")
#         stream.download(output_path)
#         print("Download completed!\n")
#     except Exception as e:
#         print(f"Error downloading {url}: {e}")

import yt_dlp

def download_video(url, output_path):
    ydl_opts = {'outtmpl': f'{output_path}/%(title)s.%(ext)s'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def download_playlist(playlist_url, output_path):
    try:
        playlist = Playlist(playlist_url)
        print(f"Downloading playlist: {playlist.title}")
        
        for video_url in playlist.video_urls:
            download_video(video_url, output_path)
        print("Playlist download completed!")
    except Exception as e:
        print(f"Error downloading playlist: {e}")

def main():
    print("YouTube Video/Playlist Downloader")
    url = input("Enter YouTube video or playlist URL: ")
    output_folder = "Downloaded_Videos"
    os.makedirs(output_folder, exist_ok=True)
    
    if 'playlist' in url:
        download_playlist(url, output_folder)
    else:
        download_video(url, output_folder)

if __name__ == "__main__":
    main()

# import os
# import yt_dlp
# import tkinter as tk
# from tkinter import filedialog, messagebox

# def download_video(url, output_path, resolution):
#     ydl_opts = {
#         'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
#         'format': f'bestvideo[height<={resolution}]+bestaudio/best'
#     }
#     try:
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             ydl.download([url])
#         messagebox.showinfo("Success", "Download completed!")
#     except Exception as e:
#         messagebox.showerror("Error", f"Download failed: {e}")

# def select_folder():
#     folder_selected = filedialog.askdirectory()
#     if folder_selected:
#         output_folder.set(folder_selected)

# def start_download():
#     url = url_entry.get()
#     res = resolution_var.get()
#     output_path = output_folder.get()
#     if not url:
#         messagebox.showerror("Error", "Please enter a YouTube URL")
#         return
#     if not output_path:
#         messagebox.showerror("Error", "Please select a download folder")
#         return
    
#     if 'playlist' in url:
#         messagebox.showinfo("Info", "Downloading playlist...")
#     else:
#         messagebox.showinfo("Info", "Downloading video...")
    
#     download_video(url, output_path, res)

# def create_gui():
#     global url_entry, output_folder, resolution_var
    
#     root = tk.Tk()
#     root.title("YouTube Video Downloader")
#     root.geometry("400x250")
    
#     tk.Label(root, text="Enter YouTube URL:").pack(pady=5)
#     url_entry = tk.Entry(root, width=50)
#     url_entry.pack(pady=5)
    
#     tk.Label(root, text="Select Resolution:").pack(pady=5)
#     resolution_var = tk.StringVar(value="1080")
#     res_options = ["360", "480", "720", "1080", "1440", "2160"]
#     res_menu = tk.OptionMenu(root, resolution_var, *res_options)
#     res_menu.pack(pady=5)
    
#     tk.Label(root, text="Select Download Folder:").pack(pady=5)
#     output_folder = tk.StringVar()
#     tk.Entry(root, textvariable=output_folder, width=40).pack(pady=5)
#     tk.Button(root, text="Browse", command=select_folder).pack(pady=5)
    
#     tk.Button(root, text="Download", command=start_download).pack(pady=10)
#     root.mainloop()

# if __name__ == "__main__":
#     create_gui()
