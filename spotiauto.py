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

def get_shuffle_preference() -> bool:
    """
    Ask the user if they want to enable shuffle mode.
    Returns True if they choose "Yes", False otherwise.
    """
    script = '''
    set shuffle_pref to choose from list {"Yes", "No"} with prompt "Do you want shuffle mode enabled?"
    if shuffle_pref is false then return "No" -- Default to "No" if user cancels
    return item 1 of shuffle_pref
    '''
    try:
        shuffle_response = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, check=True).stdout.strip()
        return shuffle_response == "Yes"
    except subprocess.CalledProcessError as e:
        logging.error(f"Error in getting shuffle preference: {e}")
        return False  # Default to shuffle off in case of error

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

def set_spotify_volume(volume: int) -> None:
    """
    Set the volume level for Spotify.
    """
    control_spotify(f'set sound volume to {volume}')

def play_playlist(playlist_uri: str, shuffle: bool) -> None:
    """
    Play a specific playlist on Spotify based on its URI, with the option to enable shuffle.
    """
    control_spotify(f'set shuffling to {str(shuffle).lower()}')  # Enable or disable shuffle
    control_spotify(f'play track "{playlist_uri}"')  # Play the playlist

def get_volume_for_mood(mood: str) -> int:
    """
    Get the volume level based on the user's mood.
    """
    volume_levels = {
        "Happy": 70,
        "Sad": 50,
        "Chill": 40,
        "Energetic": 80
    }
    return volume_levels.get(mood, 50)  # Default to 50 if mood is not found

def validate_mood_and_play_playlist(mood: Optional[str], mood_playlists: dict) -> None:
    """
    Validate the mood and play the corresponding playlist.
    Set shuffle mode and adjust the volume based on the user's preferences and mood.
    """
    if mood:
        playlist_uri = mood_playlists.get(mood)
        if playlist_uri:
            logging.info(f"Playing {mood} playlist...")
            
            # Get the shuffle preference
            shuffle = get_shuffle_preference()
            
            # Get the volume level based on the mood
            volume = get_volume_for_mood(mood)
            logging.info(f"Setting volume to {volume} for mood {mood}")
            set_spotify_volume(volume)

            # Play the playlist with the appropriate shuffle setting
            play_playlist(playlist_uri, shuffle)
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

    # Validate mood and play the corresponding playlist
    validate_mood_and_play_playlist(user_mood, mood_playlists)
