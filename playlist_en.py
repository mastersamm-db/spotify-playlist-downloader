import os
import re
import time
import urllib.request
import spotipy
import subprocess
from mutagen.easyid3 import EasyID3
from mutagen.id3 import APIC, ID3
from yt_dlp import YoutubeDL
from rich.console import Console
from spotipy.oauth2 import SpotifyClientCredentials
import urllib.parse

# Checked to conection a Internet
def check_internet_connection():
    try:
        urllib.request.urlopen('http://google.com', timeout=5)
        return True
    except urllib.request.URLError:
        return False

def get_spotify_credentials():
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

    if not client_id:
        client_id = input("Enter your SPOTIPY_CLIENT_ID: ").strip()
        subprocess.run(["powershell", "-Command", f"$env:SPOTIPY_CLIENT_ID='{client_id}'"])
        #subprocess.run(["powershell", "-Command", f"set SPOTIPY_CLIENT_ID='{client_id}'"])
        #os.environ["SPOTIPY_CLIENT_ID"] = client_id

    if not client_secret:
        client_secret = input("Enter your SPOTIPY_CLIENT_SECRET: ").strip()
        subprocess.run(["powershell", "-Command", f"$env:SPOTIPY_CLIENT_SECRET='{client_secret}'"])
        #subprocess.run(["powershell", "-Command", f"set SPOTIPY_CLIENT_SECRET='{client_secret}'"])
        #os.environ["SPOTIPY_CLIENT_SECRET"] = client_secret

    return client_id, client_secret

SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET = get_spotify_credentials()

if not SPOTIPY_CLIENT_ID or not SPOTIPY_CLIENT_SECRET:
    raise EnvironmentError("Missing Spotify API credentials. Set SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET.")

client_credentials_manager = SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
console = Console()

def main():
    if not check_internet_connection():
        raise EnvironmentError("There is no internet connection. Please check your connection and try again.")
    
    output_dir = input("Destination folder name: ").strip()
    url, url_type = validate_url(input("Enter a Spotify URL: ").strip())
    songs = [get_track_info(url)] if url_type == "track" else get_playlist_info(url)

    start_time = time.time()
    downloaded = 0

    for i, track_info in enumerate(songs, start=1):
        search_term = f"{track_info['artist_name']} {track_info['track_title']} audio"
        try:
            video_link = find_youtube(search_term)
            console.print(
                f"[magenta]({i}/{len(songs)})[/magenta] Downloading '[cyan]{track_info['artist_name']} - {track_info['track_title']}[/cyan]'..."
            )
            audio = download_yt(video_link,output_dir)
            if audio:
                set_metadata(track_info, audio)
                destination = os.path.join("../"+output_dir, os.path.basename(audio))
                os.replace(audio, destination)
                downloaded += 1
            else:
                console.print("[yellow]File already exists. Skipping...[/yellow]")

        except Exception as e:
            console.print(f"[red]Error downloading {track_info['track_title']}: {e}[/red]")

    #clean_temp_folder("../"+output_dir+"/tmp") # Optional deteleted temp folder
    end_time = time.time()

    console.print(f"\nDownload location: {os.path.abspath('../'+output_dir)}\n")
    console.print(
        f"[green]DOWNLOAD COMPLETED: {downloaded}/{len(songs)} song(s) downloaded.[/green]",
        style="on green",
    )
    console.print(
        f"Total time taken: {round(end_time - start_time)} seconds", style="on white"
    )

def validate_url(sp_url):
    match = re.match(r"^(https?://)?(open\.spotify\.com|open\.spotify\.com/intl-[a-z]{2})/(playlist|track)/.+", sp_url)
    if match:
        url_type = match.group(3)  # 'playlist' o 'track'
        return sp_url, url_type
    raise ValueError("Invalid Spotify URL")

def get_track_info(track_url):
    try:
        track = sp.track(track_url)
        return {
            "artist_name": track["artists"][0]["name"],
            "track_title": track["name"],
            "track_number": track["track_number"],
            "isrc": track["external_ids"].get("isrc", ""),
            "album_art": track["album"]["images"][1]["url"] if len(track["album"]["images"]) > 1 else "",
            "album_name": track["album"]["name"],
            "release_date": track["album"]["release_date"],
            "artists": [artist["name"] for artist in track["artists"]],
        }
    except Exception as e:
        raise ValueError(f"Failed to fetch track info: {e}")

def get_playlist_info(sp_playlist):
    try:
        pl = sp.playlist(sp_playlist)
        if not pl.get("public", False):
            raise ValueError("Playlist is private. Change it to public.")

        tracks = [item["track"] for item in sp.playlist_tracks(sp_playlist)["items"]]
        return [get_track_info(f"https://open.spotify.com/track/{track['id']}") for track in tracks if 'id' in track]
    except Exception as e:
        raise ValueError(f"Failed to fetch playlist info: {e}")

def find_youtube(query):
    try:
        search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
        response = urllib.request.urlopen(search_url)
        search_results = re.findall(r"watch\?v=(\S{11})", response.read().decode("utf-8"))
        if not search_results:
            raise ValueError("No YouTube video found for the search query.")
        return f"https://www.youtube.com/watch?v={search_results[0]}"
    except Exception as e:
        raise ValueError(f"Failed to find YouTube video: {e}")

def download_yt(yt_link,output_dir):
    try:
        # Configure options for yt-dlp
        output_dire = "../"+output_dir+"/tmp"
        os.makedirs(output_dire, exist_ok=True)

        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "256",
                }
            ],
            "ffmpeg_location": "C:\\ffmpeg\\bin",
            "outtmpl": os.path.join(output_dire, "%(title)+.100U.%(ext)s"),
            "quiet": False,
            "noplaylist": True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(yt_link, download=True)
            return os.path.join(output_dire, f"{info['title']}.mp3")

    except Exception as e:
        raise ValueError(f"Failed to download YouTube audio: {e}")

def set_metadata(metadata, file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        mp3file = EasyID3(file_path)
        mp3file.update({
            "albumartist": metadata["artist_name"],
            "artist": ", ".join(metadata["artists"]),
            "album": metadata["album_name"],
            "title": metadata["track_title"],
            "date": metadata["release_date"],
            "tracknumber": str(metadata["track_number"]),
            "isrc": metadata["isrc"],
        })
        mp3file.save()

        with urllib.request.urlopen(metadata["album_art"]) as albumart:
            audio = ID3(file_path)
            audio["APIC"] = APIC(
                encoding=3, mime="image/jpeg", type=3, desc="Cover", data=albumart.read()
            )
            audio.save()
    except Exception as e:
        raise ValueError(f"Failed to set metadata: {e}")

#def clean_temp_folder(folder): # Optional deteleted temp folder, it is not necessary since some files give an error and remain stored in the tmp folder
    #if os.path.exists(folder):
        #shutil.rmtree(folder)

if __name__ == "__main__":
    main()
