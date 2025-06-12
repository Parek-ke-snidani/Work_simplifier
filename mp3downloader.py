import subprocess

def download_mp3(video_url, output_path):
    try:
        # Use yt-dlp to download and convert to MP3
        command = [
            "yt-dlp",
            "--extract-audio",
            "--audio-format", "mp3",
            "-o", f"{output_path}/%(title)s.%(ext)s",
            video_url
        ]
        subprocess.run(command, check=True)
        print("MP3 file downloaded successfully!")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

# Example usage
video_url = "https://www.youtube.com/watch?v=ytcD6LjkEYA"  # Replace with your YouTube video URL
output_path = "C://Users//BIKEMAX//Music"  # Replace with your desired output folder path
download_mp3(video_url, output_path)
