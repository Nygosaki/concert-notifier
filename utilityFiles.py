import yaml
import os
from pathlib import Path
import json
import requests

class files:
    def __init__(self):
        self.config = {}
        self.concertsOld = []
        self.path = Path(__file__).parent
        self.configLoad()
        self.concertsOldLoad()
    
    def configLoad(self):
        if not (self.path / 'config.yaml').exists():
            print(f"\nWARN: Config file not found at {self.path / 'config.yaml'}")
            print("\nCreating a new config file")
            self.config = {
                'artists': [],
                'countries': [],
            }
            self.configUpdate()
        with open(self.path / 'config.yaml', 'r') as file:
            self.config = yaml.safe_load(file)
            file.close()
        
    
    def configUpdate(self):
        with open(self.path / 'config.yaml', 'w') as file:
            yaml.dump(self.config, file)
            file.close()
    
    def getArtists(self):
        LASTFM_API_KEY = os.getenv('LASTFM_API_KEY')
        LASTFM_USERNAME = os.getenv('LASTFM_USERNAME')

        if not LASTFM_API_KEY or not LASTFM_USERNAME: print("WARNING: LASTFM_API_KEY or LASTFM_USERNAME not found in environment variables. Last.fm integration disabled."); return []
        response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=library.getartists&api_key={LASTFM_API_KEY}&user={LASTFM_USERNAME}&format=json&limit=2000")
        data = response.text
        if response.status_code != 200: print(f"ERROR: Last.fm API request failed with status code {response.status_code}. Last.fm integration disabled."); return []
        python_list = json.loads(data)
        artists = []
        for x in python_list["artists"]["artist"]:
            if "&" not in x["name"]: artists.append(x["name"])
        return artists
    
    def concertsOldLoad(self):
        if not (self.path / '.concerts.cache').exists():
            print(f"\nWARN: Old concerts cache not found at {self.path / '.concerts.cache'}")
            print("\nCreating a new old concerts cache")
            self.concertsOld = {}
            self.concertsOldUpdate()
        with open(self.path / '.concerts.cache', 'r') as file:
            self.concertsOld = [line.strip() for line in file.readlines()]
            file.close()
    
    def concertsOldUpdate(self):
        with open(self.path / '.concerts.cache', 'w') as file:
            for concert in self.concertsOld:
                file.write(concert + '\n')
            file.close()
    

if __name__ == '__main__':
    f = files()
    print(f.config)