# Spotify downloader playlist
# English
#### Video Demo:  https://youtu.be/bp0aS67imes
#### Description: bifurcation of the @Hosea174

## About The Project

**Spotify playlist downloader** is a python 3 CLI program that downloads songs or even whole playlists from Spotify. It works by finding the YouTube URL of the music and downloading the video using a library called [yt-dlp](https://github.com/yt-dlp/yt-dlp). Then, after converting the video to mp3, the program adds different metadata of the song(Album art, Album name, artists, release date...) to the downloaded audio file using the [mutagen](https://github.com/quodlibet/mutagen) library, and [ffmpeg](https://github.com/FFmpeg/FFmpeg) library. This program also utilizes the [spotipy](https://spotipy.readthedocs.io/en/2.21.0/) library to interact with the Spotify API       

## Getting started
1. Install Python 3.x.x, download of `https://www.python.org/downloads/` for Windows or Ubuntu (Linux) `sudo apt install python3`.
2. Download ffmpeg version ffmpeg-n7.1-latest-win64-gpl-7.1.zip `https://github.com/BtbN/FFmpeg-Builds/releases` or the latest gpl version.
    - Add ffmpeg to the system PATH
    - Adding ffmpeg to the PATH allows you to use it from anywhere on your system.
    - Open Environment Variables Settings:
        Press Win + R, type sysdm.cpl and press Enter.
        Go to the "Advanced" tab and click "Environment Variables".
    - Edit the Path variable:
        Under "System Variables", select the Path variable and click Edit.
        Click New and add the path to the ffmpeg bin folder, for example:
        C:\ffmpeg\bin
    - Apply changes:
        Click OK to close all windows.
        Open a new terminal window (CMD or PowerShell) and verify that ffmpeg is running by typing:
        ffmpeg -version
3. Create a [Spotify developers account](https://developer.spotify.com/dashboard/).
4. Create an app by clicking on *create an app* and giving name and description for the app.
5. Take a note of your *Client ID* and *Client Secret*, or URL URI *https://open.spotify.com/* from the app's page and selected *Web API*.
6. Open your terminal and run `git clone https://github.com/mastersamm-db/spotify-playlist-downloader` or optionally download the zip file.
7. run `cd spotify-downloader`.
8. run in powershell `$env:SPOTIPY_CLIENT_ID='<your-client-id>'` or `set SPOTIPY_CLIENT_ID='<your-client-id>'` .
9. run in powershell `$env:SPOTIPY_CLIENT_SECRET='<your-client-secret>'` or `set SPOTIPY_CLIENT_SECRET='<your-client-secret>'`.
10. Finally, run `python playlist_en.py` and follow the instructions to download a song or a playlist from spotify.

## Prerequisites
Run the following command in the terminal after navigating to the project's directory:
```
pip install -r requirements.txt
```
# =============================================================================================================================================
# Descargar listas de reproducción de Spotify
# Español
#### Video de demostración: https://youtu.be/bp0aS67imes
#### Descripción: bifurcación de @Hosea174

## Acerca del proyecto

**Descargar listas de reproducción de Spotify** es un programa CLI de Python 3 que descarga canciones o incluso listas de reproducción completas de Spotify. Funciona buscando la URL de YouTube de la música y descargando el video usando una biblioteca llamada [yt-dlp](https://github.com/yt-dlp/yt-dlp). Luego, después de convertir el video a mp3, el programa agrega diferentes metadatos de la canción (carátula del álbum, nombre del álbum, artistas, fecha de lanzamiento...) al archivo de audio descargado usando la biblioteca [mutagen](https://github.com/quodlibet/mutagen), y la librería [ffmpeg](https://github.com/FFmpeg/FFmpeg). Este programa también utiliza la biblioteca [spotipy](https://spotipy.readthedocs.io/en/2.21.0/) para interactuar con la API de Spotify

## Primeros pasos
1. Instale Python 3.x.x, descargue `https://www.python.org/downloads/` para Windows o Ubuntu (Linux) `sudo apt install python3`.
2. Descargue ffmpeg versión ffmpeg-n7.1-latest-win64-gpl-7.1.zip `https://github.com/BtbN/FFmpeg-Builds/releases` o la ultima versión gpl,
    descomprimir en Windows siguiente ruta C:\ffmpeg\bin todos los archivos.
        - Agregar ffmpeg al PATH del sistema
        - Agregar ffmpeg al PATH te permite usarlo desde cualquier lugar en tu sistema.
        - Abre Configuración de Variables de Entorno:
            Presiona Win + R, escribe sysdm.cpl y presiona Enter.
            Ve a la pestaña "Opciones avanzadas" y haz clic en "Variables de entorno".
        - Editar la variable Path:
            En las "Variables del sistema", selecciona la variable Path y haz clic en Editar.
            Haz clic en Nuevo y agrega la ruta a la carpeta bin de ffmpeg, por ejemplo:
            C:\ffmpeg\bin
        - Aplica los cambios:
            Haz clic en Aceptar para cerrar todas las ventanas.
            Abre una nueva ventana de terminal (CMD o PowerShell) y verifica que ffmpeg esté funcionando escribiendo:
            ffmpeg -version
3. Cree una [cuenta de desarrollador de Spotify](https://developer.spotify.com/dashboard/).
4. Cree una aplicación haciendo clic en *crear una aplicación* y dando un nombre y una descripción para la aplicación.
5. Tome nota de su *Client ID* y *Client Secret*, o URL URI *https://open.spotify.com/* de la página de la aplicación y seleccionar *Web API*.
6. Abra su terminal y ejecute `git clone https://github.com/mastersamm-db/spotify-playlist-downloader` u opcionalmente descargue el archivo zip.
7. ejecute `cd spotify-downloader`.
8. ejecute en powershell `$env:SPOTIPY_CLIENT_ID='<your-client-id>'` o `set SPOTIPY_CLIENT_ID='<your-client-id>'`.
9. ejecute en powershell `$env:SPOTIPY_CLIENT_SECRET='<your-client-secret>'` o `set SPOTIPY_CLIENT_SECRET='<your-client-secret>'`.
10. Por último, ejecuta `python playlist_es.py` y sigue las instrucciones para descargar una canción o una lista de reproducción de Spotify.

## Requisitos previos
Ejecuta el siguiente comando en la terminal después de navegar al directorio del proyecto:
```
pip install -r requirements.txt
```
