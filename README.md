# concert-notifier

Get notified of your favourite artists' events near you!

## What does this do?

Whenever `main.py` is ran, it checks for any new concerts or events attended by your favourite artists in the countries you specify.  
It then sends you an email using an SMTP server with the new events, as well as events upcoming in the next 2 weeks.  
It can also output this data into a html file locally if the `--local` argument is used.

## How to use

- First, download all required packages  using `pip3 install -r requirements.txt`  
- Then, configure the `config.yaml` and `.env` files in the following format:  

```yaml
# config.yaml
artists:
- K.Flay
- The Neighbourhood
countries:
- Czech Republic
- Germany
- Poland
- Slovakia
```

```env
LASTFM_API_KEY=your_api_key_here
LASTFM_USERNAME=your_username_here
SMTP_SERVER=smtp-relay.example.com
SMTP_PORT=587
SMTP_USER=admin@example.com
SMTP_PASSWORD=thisisapassword
SENDER_NAME=ConcertsUpdate
SENDER_EMAIL=concerts@example.com
RECIPIENT_EMAIL=me@example.com
```

If you use last.fm, you can also specify your username in the .env file, and it will automatically pull all your listened to artists when the `--refresh` argument is used. This argument resets the concerts cache, forgetting what events you have already been notified of, and pulls your artists from last.fm.  

- Now, you can run `python3 main.py {args}`!

## Requirements

- If you want to use the last.fm integration, you need to add an API key as well. You can acquire it at [https://www.last.fm/api/authentication](https://www.last.fm/api/authentication) if you don't already have one.  
- If you want to use the email integration, you need to specify SMTP server information.  

## How does it look?

![image](https://github.com/user-attachments/assets/1e3a3c7a-6d38-457c-8021-457b06f5cfbd)

## How does it work? And why?

Spotify and Songkick never notified me about al lthe concerts and artists I care about, so I made this to give me information for all the artists I could ever want! It can pull artists automatically from your last.fm library, or you can manually add them.  
It scrapes multiple songkick servises and for the artists you want. It then gets their events, and filters them by country :).  
It then sends you this info via a SMTP TLS connection to an email server. The sender display information can also thus be configured.  
It can also just save the html content of the email locally into it's parent folder if you don't have a server and domain to use.  
