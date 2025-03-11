import os
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import yt_dlp

def download_video(url, download_path='downloads'):
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'{download_path}/%(title)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_audio(url, download_path='downloads'):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{download_path}/%(title)s.%(ext)s',
        #'postprocessors': [{
         #   'key': 'FFmpegExtractAudio',
          #  'preferredcodec': 'mp3',
           # 'preferredquality': '192',
        #}],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def start_download(choice):
    url = simpledialog.askstring("Input", "Enter the video URL:")
    if not url:
        messagebox.showerror("Error", "No URL entered.")
        return

    download_path = 'downloads'
    os.makedirs(download_path, exist_ok=True)

    try:
        if choice == "MP3":
            download_audio(url, download_path)
            messagebox.showinfo("Success", "Audio downloaded successfully!")
        elif choice == "MP4":
            download_video(url, download_path)
            messagebox.showinfo("Success", "Video downloaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# GUI setup
root = tk.Tk()
root.title("YouTube Downloader")

frame = tk.Frame(root)
frame.pack(pady=20, padx=20)

label = tk.Label(frame, text="Choose the format for download:", font=("Arial", 12))
label.pack()

mp3_button = tk.Button(frame, text="Download MP3", command=lambda: start_download("MP3"), width=20)
mp3_button.pack(pady=5)

mp4_button = tk.Button(frame, text="Download MP4", command=lambda: start_download("MP4"), width=20)
mp4_button.pack(pady=5)

root.mainloop()
