# encoding=utf8
import SpotifyWrap as spotify

#Finds our average popularity rating for the tracks in a given spotify playlist
def average_popularity(playlist="spotify:playlist:4hJ9abkxS8k0zqDHgdizbb"):
    # Get popularity ratings for each song
    results = spotify.get_popularities(playlist)
    # Check if we got valid data from Spotify
    if results:
        sum = 0.0
        # Loop through every popularity rating
        for number in results:
            # Add to the sum
            sum += number
        # Find the average popularities of the playlist
        average = sum/len(results)
        return average
    else:
        return None
