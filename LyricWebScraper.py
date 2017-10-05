#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# adapted from: https://bigishdata.com/2016/09/27/getting-song-lyrics-from-geniuss-api-scraping/
# to find the artist ID, go to https://docs.genius.com/#/authentication-h1
# and search for a song by that artist, then find the "id" tag in the results
import sys
import requests
import json
from bs4 import BeautifulSoup
sys.path.append('C:\PythonProjects\PythonUtilities')
import CFGFileHelper

cfgpath = 'C:\PythonProjects\Private\lyricgeniuscredentials.ini'
credentialdict = CFGFileHelper.read(cfgpath,'credentials')

base_url = "http://api.genius.com"
token = 'Bearer '+ credentialdict['client_access_token']
headers = {'Authorization': token}

# the national
artist_id = '658'
filename = "thenational2.txt"

#tom petty
artist_id = '67932'
filename = "tompetty.txt"

def lyrics_from_song_api_path(song_api_path):
  song_url = base_url + song_api_path
  response = requests.get(song_url, headers=headers)
  json = response.json()
  path = json["response"]["song"]["path"]
  #gotta go regular html scraping... come on Genius
  page_url = "https://genius.com" + path
  page = requests.get(page_url)
  html = BeautifulSoup(page.text, "html.parser")
  #remove script tags that they put in the middle of the lyrics
  [h.extract() for h in html('script')]
  #at least Genius is nice and has a tag called 'lyrics'!
  lyrics = html.find("div", class_="lyrics").get_text() #updated css where the lyrics are based in HTML
  lyrics.replace('\n', ' ')
  return lyrics



def pull_lyrics():
    with open(filename, "w", encoding="utf-8") as outfile:
        nextpage = 1
        while nextpage != None:
            print("Downloading page "+str(nextpage))
            url = base_url + "/artists/"+artist_id+ "/songs?per_page=50&page="+str(nextpage)
            response = requests.get(url, headers=headers)
            json = response.json()
            nextpage = json["response"]["next_page"]
            for song in json["response"]["songs"]:
                print(song["title"]+" by "+song["primary_artist"]["name"])
                song_api_path = song["api_path"]
                lyrics = lyrics_from_song_api_path(song_api_path)
                outfile.write(lyrics)
    outfile.Close()

if __name__ == "__main__":
    pull_lyrics()


