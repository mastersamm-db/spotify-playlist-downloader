import os
import re
import shutil
import time
import urllib.parse
import urllib.request
import requests
import spotipy
from moviepy import AudioFileClip
from mutagen.easyid3 import EasyID3
from mutagen.id3 import APIC, ID3
#from pytube import YouTube
from yt_dlp import *
from rich.console import Console
from spotipy.oauth2 import SpotifyClientCredentials

# Inicializa las credenciales de Spotify desde variables de entorno
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")

if not SPOTIPY_CLIENT_ID or not SPOTIPY_CLIENT_SECRET:
    raise EnvironmentError("Faltan credenciales de la API de Spotify. Establezca SPOTIPY_CLIENT_ID y SPOTIPY_CLIENT_SECRET.")

client_credentials_manager = SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
console = Console()

def main():
    #url = validate_url(input("Ingrese una URL de Spotify: ").strip())
    #songs = [get_track_info(url)] if "track" in url else get_playlist_info(url)
    url, url_type = validate_url(input("Ingrese una URL de Spotify: ").strip())
    songs = [get_track_info(url)] if url_type == "track" else get_playlist_info(url)
    
    start_time = time.time()
    downloaded = 0

    for i, track_info in enumerate(songs, start=1):
        search_term = f"{track_info['artist_name']} {track_info['track_title']} audio"
        try:
            video_link = find_youtube(search_term)
            console.print(f"[magenta]({i}/{len(songs)})[/magenta] Descargando '[cyan]{track_info['artist_name']} - {track_info['track_title']}[/cyan]'...")
            audio = download_yt(video_link)

            if audio:
                set_metadata(track_info, audio)
                destination = os.path.join("../musicshazam", os.path.basename(audio))
                os.replace(audio, destination)
                downloaded += 1
            else:
                console.print("[yellow]El archivo ya existe. Saltando...[/yellow]")
        except Exception as e:
            console.print(f"[red]Error en {track_info['track_title']}: {e}[/red]")

    #clean_temp_folder("../musicshazam/tmp") # Elimina la carpeta temporal
    end_time = time.time()

    console.print(f"\nUbicación de descarga: {os.path.abspath('../musicshazam')}\n")
    console.print(f"[green]DESCARGA COMPLETADA: {downloaded}/{len(songs)} canción(es) descargada(s).[/green]", style="on green")
    console.print(f"Tiempo total tomado: {round(end_time - start_time)} segundos", style="on white")

#def validate_url(sp_url):
    #if re.match(r"^(https?://)?open\.spotify\.com/(playlist|track)/.+", sp_url):
        #return sp_url
    #raise ValueError("URL de Spotify no válida")
def validate_url(sp_url):
    match = re.match(r"^(https?://)?(open\.spotify\.com|open\.spotify\.com/intl-[a-z]{2})/(playlist|track)/.+", sp_url)
    if match:
        url_type = match.group(3)  # 'playlist' o 'track'
        return sp_url, url_type
    raise ValueError("URL de Spotify no válida")

def get_track_info(track_url):
    try:
        track = sp.track(track_url)
        return {
            "artist_name": track["artists"][0]["name"],
            "track_title": track["name"],
            "track_number": track["track_number"],
            "isrc": track["external_ids"].get("isrc", ""),
            "album_art": track["album"]["images"][1]["url"],
            "album_name": track["album"]["name"],
            "release_date": track["album"]["release_date"],
            "artists": [artist["name"] for artist in track["artists"]],
        }
    except Exception as e:
        raise ValueError(f"Fallo al obtener información de la pista: {e}")

def get_playlist_info(sp_playlist):
    try:
        pl = sp.playlist(sp_playlist)
        if not pl.get("public", False):
            raise ValueError("La lista de reproducción es privada. Cambia a pública.")
        
        tracks = [item["track"] for item in sp.playlist_tracks(sp_playlist)["items"]]
        return [get_track_info(f"https://open.spotify.com/track/{track['id']}") for track in tracks]
    except Exception as e:
        raise ValueError(f"Fallo al obtener información de la lista de reproducción: {e}")

def find_youtube(query):
    try:
        search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
        response = urllib.request.urlopen(search_url)
        search_results = re.findall(r"watch\?v=(\S{11})", response.read().decode('utf-8'))
        return f"https://www.youtube.com/watch?v={search_results[0]}"
    except Exception as e:
        raise ValueError(f"Fallo al encontrar video en YouTube: {e}")

def download_yt(yt_link):
    try:
        # Configura las opciones para yt-dlp
        output_dir = "../musicshazam/tmp2"
        os.makedirs(output_dir, exist_ok=True)

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
            "outtmpl": os.path.join(output_dir, "%(title)+.100U.%(ext)s"),
            "quiet": False,
            "noplaylist": True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(yt_link, download=True)
            return os.path.join(output_dir, f"{info['title']}.mp3")

    except Exception as e:
        raise ValueError(f"No se pudo descargar el audio de YouTube: {e}")

def set_metadata(metadata, file_path):
    try:
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
                encoding=3, mime="image/jpeg", type=3, desc="Cover", data=albumart.read())
            
            audio.save()
    except Exception as e:
        raise ValueError(f"Fallo al establecer metadatos: {e}")

#def clean_temp_folder(folder): # Elimina la carpeta temporal
    #if os.path.exists(folder):
        #shutil.rmtree(folder)

if __name__ == "__main__":
    main()
