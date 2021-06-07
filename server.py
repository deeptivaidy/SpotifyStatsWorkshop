#!/usr/bin/env python
# -*- coding: utf-8 -*-

#       _                              
#      | |                             
#    __| |_ __ ___  __ _ _ __ ___  ___ 
#   / _` | '__/ _ \/ _` | '_ ` _ \/ __|
#  | (_| | | |  __/ (_| | | | | | \__ \
#   \__,_|_|  \___|\__,_|_| |_| |_|___/ .
#
# A 'Fog Creek'–inspired demo by Kenneth Reitz™


from flask import Flask, request, render_template, jsonify
import os
import spotify_stats
import SpotifyWrap as spotify

# Support for gomix's 'front-end' and 'back-end' UI.
app = Flask(__name__, static_folder='public', template_folder='views')

# Set the app secret key from the secret environment variables.
app.secret = os.environ.get('SECRET')

# Dream database. Store dreams in memory for now. 
DREAMS = ['United States Top 50: 85.2/100 for 50 songs']


@app.after_request
def apply_kr_hello(response):
    """Adds some headers to all responses."""
  
    # Made by Kenneth Reitz. 
    if 'MADE_BY' in os.environ:
        response.headers["X-Was-Here"] = os.environ.get('MADE_BY')
    
    # Powered by Flask. 
    response.headers["X-Powered-By"] = os.environ.get('POWERED_BY')
    return response


@app.route('/')
def homepage():
    """Displays the homepage."""
    return render_template('index.html')
    
@app.route('/stats', methods=['GET', 'POST'])
def stats():
    """Simple API endpoint for dreams. 
    In memory, ephemeral, like real dreams.
    """
    if request.method == 'POST':
      print(len(request.args))
    # Add a popularity stat to the in-memory database, if given. 
    if 'playlist' in request.args:
        playlist_name = spotify.get_playlist_name(request.args['playlist'])
        average_popularity = spotify_stats.average_popularity(request.args['playlist'])
        if playlist_name and average_popularity:
            playlist_size = len(spotify.get_tracks(request.args['playlist']))
            DREAMS.append(str(playlist_name)+ ": " +str(average_popularity) + "/100 for "+ str(playlist_size) + " songs")
            print(request.args['playlist'])
        else:
            DREAMS.append(request.args['playlist'] + " did not work :( Try again!")
    
    # Return the list of previous values. 
    return jsonify(DREAMS)

if __name__ == '__main__':
    app.run(debug=True)