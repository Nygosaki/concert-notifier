import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
import datetime
import sys
import os

def sendEmail(events: dict):

    # Build the HTML content dynamically.
    html_content = """
    <!DOCTYPE html>
    <html xmlns="http://www.w3.org/1999/xhtml" style="margin:0;padding:0">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style type="text/css">
        @media only screen and (min-device-width: 481px) {
            div[id="main"] {
            width: 480px !important;
            }
        }
        </style>
        <style type="text/css">
        @font-face {
            font-family: SpotifyMixUI;
            font-weight: 700;
            font-display: swap;
            src: url('https://encore.scdn.co/fonts/SpotifyMixUI-Bold-4264b799009b1db5c491778b1bc8e5b7.woff2') format('woff2');
        }

        @font-face {
            font-family: SpotifyMixUI;
            font-weight: 400;
            font-display: swap;
            src: url('https://encore.scdn.co/fonts/SpotifyMixUI-Regular-cc3b1de388efa4cbca6c75cebc24585e.woff2') format('woff2');
        }

        @font-face {
            font-family: SpotifyMixUITitle;
            font-weight: 800;
            font-display: swap;
            src: url('https://encore.scdn.co/fonts/SpotifyMixUITitle-Extrabold-ba6c73cd7f82c81e49cf2204017803ed.woff2') format('woff2');
        }

        @font-face {
            font-family: SpotifyMixUITitle;
            font-weight: 700;
            font-display: swap;
            src: url('https://encore.scdn.co/fonts/SpotifyMixUITitle-Bold-37290f1de77f297fcc26d71e9afcf43f.woff2') format('woff2');
        }
        </style>
        <style>
        * {
            border: none;
            padding: 0;
            margin: 0;
            font-family: SpotifyMixUI, Helvetica, Arial, sans-serif;
        }

        table {
            border-collapse: collapse;
        }

        .container {
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }

        .artist-info {
            display: flex;
            flex-direction: row;
            align-items: center;
        }

        .artist-info img {
            max-width: 150px;
            border-radius: 50%;
            margin-right: 20px;
        }

        .artist-details {
            flex: 1;
        }

        .artist-details h1 {
            font-size: 24px;
            margin-bottom: 10px;
        }

        .tour-dates {
            margin-top: 20px;
        }

        .tour-dates h2 {
            font-size: 20px;
            margin-bottom: 10px;
        }

        .tour-dates ul {
            list-style-type: none;
            padding: 0;
        }

        .tour-dates ul li {
            margin-bottom: 5px;
        }
        </style>
    </head>
    <body topmargin="0" leftmargin="0" rightmargin="0" bottommargin="0" marginheight="0" marginwidth="0" style="-webkit-font-smoothing:antialiased;width:100% !important;-webkit-text-size-adjust:none;margin:0;padding:0;font-family:SpotifyMixUI, Helvetica, Arial, sans-serif">
    """

    subject = "New: "
    for artist in events:
        if events[artist].__len__() == 0: continue
        subject += f"{artist}, "
        html_content += f"""
            <div class="container">
            <div class="artist-info">
                <img src="{events[artist][0]['raw'][0]['image']}" alt="Artist Image" type="image/jpeg">
                <div class="artist-details">
                <h1>{artist}</h1>
                <p>{(", ".join(events[artist][0]["raw"][0]["performer"][0]["genre"])).replace("_", " ")}</p>
                </div>
            </div>
            <div class="tour-dates">
                <h2>Tour Dates</h2>
                <ul>
            """
        for event in events[artist]:
            html_content += f"""
                <li>{event["raw"][0]["startDate"][:10]} - {event["raw"][0]["location"]["@type"]}, {event["raw"][0]["location"]["name"]}, {event["location"]}</li>
            """
        pass
        
        html_content += """
            </ul>
    </div>
    </div>
    """

    subject = subject[:-2]  # Remove the trailing comma and space
    if subject.__len__() > 80:
        subject = subject[:77] + "..."

    html_content += """
    </body>
    </html>
    """

    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = os.getenv("SMTP_PORT")
    USER = os.getenv("SMTP_USER")
    PASSWORD = os.getenv("SMTP_PASSWORD")
    SENDER_NAME = os.getenv("SENDER_NAME")
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

    if "--local" in sys.argv or not SMTP_SERVER or not SMTP_PORT or not USER or not PASSWORD or not SENDER_NAME or not SENDER_EMAIL or not RECIPIENT_EMAIL:
        with open("output.html", "w") as file:
            file.write(html_content)
        print("\nHTML content written to output.html")
        return

    # Create the email message container (multipart/alternative).
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = formataddr((SENDER_NAME, SENDER_EMAIL))
    message["To"] = RECIPIENT_EMAIL

    # Optionally, you can include a plain-text version as a fallback.
    plain_text = "Please load using HTML."

    # Attach the plain text and HTML parts.
    part1 = MIMEText(plain_text, "plain")
    part2 = MIMEText(html_content, "html")
    message.attach(part1)
    message.attach(part2)

    # Send the email using SMTP.
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(USER, PASSWORD)
            server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, message.as_string())
        print("\nEmail sent successfully!")
    except Exception as e:
        print(f"\nError sending email: {e}")
        with open("output.html", "w") as file:
            file.write(html_content)
        print("\nHTML content written to output.html")

if __name__ == "__main__":
    data = {'bbno$': [{'location': 'Cologne, Germany', 'date': datetime.datetime(2025, 5, 4, 20, 0), 'raw': [{'@context': 'http://schema.org', '@type': 'MusicEvent', 'name': 'bbno$ @ Live Music Hall', 'url': 'https://www.songkick.com/concerts/42295833-bbnos-at-live-music-hall?utm_medium=organic&utm_source=microformat', 'image': 'https://images.sk-static.com/images/media/profile_images/artists/9033619/huge_avatar', 'eventAttendanceMode': 'https://schema.org/OfflineEventAttendanceMode', 'location': {'@type': 'Place', 'address': {'@type': 'PostalAddress', 'addressLocality': 'Cologne', 'addressCountry': 'Germany', 'streetAddress': 'Lichtstraße 30', 'postalCode': '50825'}, 'name': 'Live Music Hall', 'sameAs': 'http://www.livemusichall.de/', 'geo': {'@type': 'GeoCoordinates', 'latitude': 50.94919, 'longitude': 6.91008}}, 'eventStatus': 'https://schema.org/EventScheduled', 'startDate': '2025-05-04T20:00:00', 'endDate': '2025-05-04', 'performer': [{'@type': 'MusicGroup', 'name': 'bbno$', 'genre': ['r_and_b', 'hip_hop'], 'sameAs': 'https://www.songkick.com/artists/9033619-bbnos?utm_medium=organic&utm_source=microformat'}], 'description': 'bbno$ at Live Music Hall at 2025-05-04T20:00:00+0200', 'organizer': {'@type': 'Organization', 'name': 'bbno$', 'url': 'https://www.songkick.com/concerts/42295833-bbnos-at-live-music-hall?utm_medium=organic&utm_source=microformat'}, 'offers': [{'@type': 'Offer', 'url': 'http://www.songkick.com/concerts/42295833-bbnos-at-live-music-hall?utm_medium=organic&utm_source=microformat'}]}]}, {'location': 'Prague, Czech Republic', 'date': datetime.datetime(2025, 5, 11, 19, 30), 'raw': [{'@context': 'http://schema.org', '@type': 'MusicEvent', 'name': 'bbno$ @ Roxy', 'url': 'https://www.songkick.com/concerts/42295838-bbnos-at-roxy?utm_medium=organic&utm_source=microformat', 'image': 'https://images.sk-static.com/images/media/profile_images/artists/9033619/huge_avatar', 'eventAttendanceMode': 'https://schema.org/OfflineEventAttendanceMode', 'location': {'@type': 'Place', 'address': {'@type': 'PostalAddress', 'addressLocality': 'Prague', 'addressCountry': 'Czech Republic', 'streetAddress': 'Dlouhá 33', 'postalCode': '11000'}, 'name': 'Roxy', 'sameAs': 'https://www.roxy.cz/', 'geo': {'@type': 'GeoCoordinates', 'latitude': 50.09068, 'longitude': 14.42582}}, 'eventStatus': 'https://schema.org/EventScheduled', 'startDate': '2025-05-11T19:30:00', 'endDate': '2025-05-11', 'performer': [{'@type': 'MusicGroup', 'name': 'bbno$', 'genre': ['r_and_b', 'hip_hop'], 'sameAs': 'https://www.songkick.com/artists/9033619-bbnos?utm_medium=organic&utm_source=microformat'}], 'description': 'bbno$ at Roxy at 2025-05-11T19:30:00+0200', 'organizer': {'@type': 'Organization', 'name': 'bbno$', 'url': 'https://www.songkick.com/concerts/42295838-bbnos-at-roxy?utm_medium=organic&utm_source=microformat'}, 'offers': [{'@type': 'Offer', 'url': 'http://www.songkick.com/concerts/42295838-bbnos-at-roxy?utm_medium=organic&utm_source=microformat'}]}]}, {'location': 'Berlin, Germany', 'date': datetime.datetime(2025, 5, 13, 20, 0), 'raw': [{'@context': 'http://schema.org', '@type': 'MusicEvent', 'name': 'bbno$ @ Huxleys Neue Welt', 'url': 'https://www.songkick.com/concerts/42295832-bbnos-at-huxleys-neue-welt?utm_medium=organic&utm_source=microformat', 'image': 'https://images.sk-static.com/images/media/profile_images/artists/9033619/huge_avatar', 'eventAttendanceMode': 'https://schema.org/OfflineEventAttendanceMode', 'location': {'@type': 'Place', 'address': {'@type': 'PostalAddress', 'addressLocality': 'Berlin', 'addressCountry': 'Germany', 'streetAddress': 'Hasenheide 107-113', 'postalCode': '10967'}, 'name': 'Huxleys Neue Welt', 'sameAs': 'http://www.huxleysneuewelt.com/', 'geo': {'@type': 'GeoCoordinates', 'latitude': 52.48642, 'longitude': 13.42153}}, 'eventStatus': 'https://schema.org/EventScheduled', 'startDate': '2025-05-13T20:00:00', 'endDate': '2025-05-13', 'performer': [{'@type': 'MusicGroup', 'name': 'bbno$', 'genre': ['r_and_b', 'hip_hop'], 'sameAs': 'https://www.songkick.com/artists/9033619-bbnos?utm_medium=organic&utm_source=microformat'}], 'description': 'bbno$ at Huxleys Neue Welt at 2025-05-13T20:00:00+0200', 'organizer': {'@type': 'Organization', 'name': 'bbno$', 'url': 'https://www.songkick.com/concerts/42295832-bbnos-at-huxleys-neue-welt?utm_medium=organic&utm_source=microformat'}, 'offers': [{'@type': 'Offer', 'url': 'http://www.songkick.com/concerts/42295832-bbnos-at-huxleys-neue-welt?utm_medium=organic&utm_source=microformat'}]}]}, {'location': 'Warsaw, Poland', 'date': datetime.datetime(2025, 5, 14, 18, 0), 'raw': [{'@context': 'http://schema.org', '@type': 'MusicEvent', 'name': 'bbno$ @ Palladium', 'url': 'https://www.songkick.com/concerts/42295848-bbnos-at-palladium?utm_medium=organic&utm_source=microformat', 'image': 'https://images.sk-static.com/images/media/profile_images/artists/9033619/huge_avatar', 'eventAttendanceMode': 'https://schema.org/OfflineEventAttendanceMode', 'location': {'@type': 'Place', 'address': {'@type': 'PostalAddress', 'addressLocality': 'Warsaw', 'addressCountry': 'Poland', 'streetAddress': 'Złota 9', 'postalCode': '02-089'}, 'name': 'Palladium', 'sameAs': 'http://www.palladium.art.pl/', 'geo': {'@type': 'GeoCoordinates', 'latitude': 52.23272, 'longitude': 21.01147}}, 'eventStatus': 'https://schema.org/EventScheduled', 'startDate': '2025-05-14T18:00:00', 'endDate': '2025-05-14', 'performer': [{'@type': 'MusicGroup', 'name': 'bbno$', 'genre': ['r_and_b', 'hip_hop'], 'sameAs': 'https://www.songkick.com/artists/9033619-bbnos?utm_medium=organic&utm_source=microformat'}], 'description': 'bbno$ at Palladium at 2025-05-14T18:00:00+0200', 'organizer': {'@type': 'Organization', 'name': 'bbno$', 'url': 'https://www.songkick.com/concerts/42295848-bbnos-at-palladium?utm_medium=organic&utm_source=microformat'}, 'offers': [{'@type': 'Offer', 'url': 'http://www.songkick.com/concerts/42295848-bbnos-at-palladium?utm_medium=organic&utm_source=microformat'}]}]}]}
    sendEmail(data)