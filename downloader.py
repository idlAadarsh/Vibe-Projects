import yt_dlp

# Change this path to your desired download folder
DOWNLOAD_PATH = '/data/data/com.termux/files/home/storage/downloads'

def download_video(url):
    with yt_dlp.YoutubeDL({}) as ydl:
        info = ydl.extract_info(url, download=False)  # get info without downloading
        formats = info['formats']

        # Filter formats that have both video and audio
        video_formats = [f for f in formats if f.get('vcodec') != 'none']

        # Display available resolutions
        print("\nAvailable Resolutions:")
        for i, f in enumerate(video_formats):
            res = f"{f.get('height')}p" if f.get('height') else 'Unknown'
            print(f"{i+1}. {res} | {f.get('ext')} | Format ID: {f.get('format_id')}")

        choice = int(input("\nSelect resolution number: ")) - 1
        selected_format = video_formats[choice]['format_id']

        ydl_opts = {
            'format': selected_format,
            'outtmpl': f'{DOWNLOAD_PATH}/%(title)s.%(ext)s',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    print("✅ Video download completed!\n")


def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{DOWNLOAD_PATH}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print("✅ Audio download completed!\n")


def main():
    print("🎬 YouTube Downloader using yt-dlp 🎬")
    print("1. Download Video (choose resolution)")
    print("2. Download Audio (MP3)")
    print("3. Download Playlist (Video)")
    choice = input("Enter your choice (1/2/3): ")

    url = input("Enter YouTube URL: ")

    if choice == '1':
        download_video(url)
    elif choice == '2':
        download_audio(url)
    elif choice == '3':
        # Playlists are handled automatically by yt-dlp
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'{DOWNLOAD_PATH}/%(title)s.%(ext)s'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("✅ Playlist download completed!\n")
    else:
        print("❌ Invalid choice. Exiting.")


if __name__ == "__main__":
    main()
