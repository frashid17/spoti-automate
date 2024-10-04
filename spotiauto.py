import subprocess
import sys
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)

def get_mood() -> Optional[str]:
    """
    Display a pop-up dialog to ask the user for their mood (happy, sad, etc.).
    Returns the mood as a string or None if the user cancels.
    """
    script = '''
    set mood to choose from list {"Happy", "Sad", "Chill", "Energetic"} with prompt "How are you feeling today?"
    if mood is false then return "None" -- If the user cancels, return "None"
    return item 1 of mood
    '''
    try:
        mood = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, check=True).stdout.strip()
        return mood if mood != "None" else None
    except subprocess.CalledProcessError as e:
        logging.error(f"Error in getting mood: {e}")
        return None

def control_spotify(command: str) -> None:
    """
    Use AppleScript to control the Spotify desktop app on macOS.
    """
    script = f'tell application "Spotify" to {command}'
    try:
        subprocess.run(['osascript', '-e', script], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to send command to Spotify: {e}")
        sys.exit(1)

def play_playlist(playlist_uri: str) -> None:
    """
    Play a specific playlist on Spotify based on its URI, with shuffle mode enabled.
    """
    control_spotify('set shuffling to true')  # Turn on shuffle
    control_spotify(f'play track "{playlist_uri}"')  # Play the playlist

def validate_mood_and_play_playlist(mood: Optional[str], mood_playlists: dict) -> None:
    """
    Validate the mood and play the corresponding playlist.
    If no mood or invalid mood is given, print a message and exit.
    """
    if mood:
        playlist_uri = mood_playlists.get(mood)
        if playlist_uri:
            logging.info(f"Playing {mood} playlist with shuffle...")
            play_playlist(playlist_uri)
        else:
            logging.warning(f"No playlist found for mood: {mood}")
    else:
        logging.info("No mood selected. Exiting.")
        sys.exit(0)

if __name__ == "__main__":
    # Define playlists for each mood
    mood_playlists = {
        "Happy": "spotify:playlist:37i9dQZF1DXdPec7aLTmlC",  # Replace with your playlist URI
        "Sad": "spotify:playlist:37i9dQZF1DWVrtsSlLKzro",    # Replace with your playlist URI
        "Chill": "spotify:playlist:37i9dQZF1DX4WYpdgoIcn6",  # Replace with your playlist URI
        "Energetic": "spotify:playlist:37i9dQZF1DX76Wlfdnj7AP" # Replace with your playlist URI
    }

    # Get the user's mood
    user_mood = get_mood()

    # Validate mood and play the corresponding playlist with shuffle
    validate_mood_and_play_playlist(user_mood, mood_playlists)
