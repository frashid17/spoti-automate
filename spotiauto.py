import subprocess

def get_mood():
    """
    Display a pop-up dialog to ask the user for their mood (happy, sad, etc.).
    Returns the mood as a string.
    """
    script = '''
    set mood to choose from list {"Happy", "Sad", "Chill", "Energetic"} with prompt "How are you feeling today?"
    if mood is false then return "None" -- If the user cancels, return "None"
    return item 1 of mood
    '''
    mood = subprocess.run(['osascript', '-e', script], capture_output=True, text=True).stdout.strip()
    return mood

def control_spotify(command):
    """
    Use AppleScript to control the Spotify desktop app on macOS.
    """
    script = f'tell application "Spotify" to {command}'
    subprocess.run(['osascript', '-e', script])

def play_playlist(playlist_uri):
    """
    Play a specific playlist on Spotify based on its URI.
    """
    control_spotify(f'play track "{playlist_uri}"')

# Define playlists for each mood
mood_playlists = {
    "Happy": "spotify:playlist:37i9dQZF1DXdPec7aLTmlC",  # Replace with your playlist URI
    "Sad": "spotify:playlist:37i9dQZF1DWVrtsSlLKzro",    # Replace with your playlist URI
    "Chill": "spotify:playlist:37i9dQZF1DX4WYpdgoIcn6",  # Replace with your playlist URI
    "Energetic": "spotify:playlist:37i9dQZF1DX76Wlfdnj7AP" # Replace with your playlist URI
}

# Get the user's mood
mood = get_mood()

# If the user didn't cancel, play the corresponding playlist
if mood != "None":
    playlist_uri = mood_playlists.get(mood)
    if playlist_uri:
        print(f"Playing {mood} playlist...")
        play_playlist(playlist_uri)
    else:
        print(f"No playlist found for mood: {mood}")
else:
    print("No mood selected. Exiting.")
