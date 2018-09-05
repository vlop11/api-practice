#coding=utf-8
import os
import os.path
import requests
import requests_toolbelt.adapters.appengine
import json
import webapp2
import jinja2

# Use the App Engine Requests adapter. This makes sure that Requests uses
# URLFetch.
requests_toolbelt.adapters.appengine.monkeypatch()

jinja_current_directory = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True)

class HomePage(webapp2.RequestHandler):
    def get(self):
        # render the home screen
        home_template = jinja_current_directory.get_template('templates/home.html')
        self.response.write(home_template.render())

class LyricsPage(webapp2.RequestHandler):
    def post(self):
        # grabs input from HTML form
        track = self.request.get('track_title')
        artist = self.request.get('artist_name')

        # GET request to the api
        r = requests.get('https://api.lyrics.ovh/v1/' + artist + '/' + track)

        # if the request goes through succesfully
        if r.status_code == 200:

            # brings back json data as a python dict
            json_data = json.loads(r.text)

            # gets value at the specified key 'lyrics' & encodes string
            song_lyrics = json_data['lyrics'].encode()

            lyrics_dict = {"lyrics": song_lyrics}
        # if no lyrics are found, do this
        else:
            lyrics_dict = {"error": "No lyrics were found. Search again please"}

        lyrics_template = jinja_current_directory.get_template('templates/lyrics.html')
        self.response.write(lyrics_template.render(lyrics_dict))

app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/lyrics', LyricsPage)
], debug=True)
