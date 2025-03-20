import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
from concurrent.futures import ThreadPoolExecutor
import threading

class personalizedConcerts:
    def __init__(self, files: object):
        self.f = files
        self.events = {}
        self.eventsImportant = {}
        self.indexArtist = 0
        self.indexArtistLock = threading.Lock()
        self.getConcerts()
        self.getConcertsImportant()
    
    def getPage(self, url: str):
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.3"})
        return resp.text if resp.status_code == 200 else None
    
    def getArtistURL(self, artist: str) -> str | None:
        query = requests.utils.quote(artist)
        soup = BeautifulSoup(
            self.getPage(f"https://www.songkick.com/search?query={query}&type=artists"), "html.parser"
        )
        artist_tag = soup.select_one("li.artist a")
        return f"https://www.songkick.com{artist_tag['href']}" if artist_tag else None
    
    def fetchConcertsForArtist(self, artist):
        artistURL = self.getArtistURL(artist)
        if not artistURL:
            print(f"\nWARN: {artist} not found")
            self.f.config['artists'].remove(artist)
            self.f.configUpdate()
            return

        soup = BeautifulSoup(self.getPage(f"{artistURL}/calendar"), "html.parser")
        artistEvents = soup.select("li.event-listing")
        if not artistEvents: return
        self.events[artist] = []
        for event in artistEvents:
            eventParse = {"location": event.select_one(".primary-detail").get_text(strip=True)}
            if eventParse["location"].lower().split(",")[-1][1:] not in [country.lower() for country in self.f.config['countries']]: continue
            eventParse["date"] = datetime.fromisoformat(event.select_one("time")["datetime"]).replace(tzinfo=None)
            if eventParse["date"] < (datetime.now() + timedelta(days=1)) or eventParse["date"] > (datetime.now() + timedelta(days=180)): continue
            eventParse["raw"] = json.loads(str(event.find("script"))[35:-9])
            self.events[artist].append(eventParse)
        with self.indexArtistLock:
            self.indexArtist += 1
            print(f"\r({self.indexArtist}/{len(self.f.config['artists'])}) - {round((self.indexArtist/len(self.f.config['artists']))*100)}%", end='')
    
    def getConcerts(self):
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(self.fetchConcertsForArtist, self.f.config['artists'])
        print("\nConcert fetching completed.")
    
    def getConcertsImportant(self):
        for artist in self.events:
            if self.events[artist].__len__() == 0: continue
            self.eventsImportant[artist] = []
            for event in self.events[artist]:
                if str(event["raw"]) in self.f.concertsOld and event["date"] > (datetime.now() + timedelta(weeks=2)): continue
                self.f.concertsOld.append(str(event["raw"]))
                self.eventsImportant[artist].append(event)
        self.f.concertsOldUpdate()



if __name__ == "__main__":
    from utilityFiles import files
    f = files()
    perCon = personalizedConcerts(f)
    print(perCon.events)