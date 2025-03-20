from utilityFiles import files
from concertsPersonalized import personalizedConcerts
from notify import sendEmail
import sys
import os
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    f = files()
    if "--refresh" in sys.argv:
        print("Flushing")
        f.config["artists"] = f.getArtists()
        f.configUpdate()
        f.concertsOld = []
        f.concertsOldUpdate()
    perCon = personalizedConcerts(f)
    sendEmail(perCon.eventsImportant)