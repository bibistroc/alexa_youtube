[![codecov](https://codecov.io/gh/bibistroc/alexa_youtube/branch/master/graph/badge.svg)](https://codecov.io/gh/bibistroc/alexa_youtube) [![Build Status](https://travis-ci.org/bibistroc/alexa_youtube.svg?branch=master)](https://travis-ci.org/bibistroc/alexa_youtube)

# Echo Dot Youtube Skill

This skill is intented for personal use only (in development mode), is highly recommended to not push it on amazon marketplace.

# Information

I wrote and tested this code on a Raspberry Pi 2 b+ model. It should also work an Raspberry Pi 3 on any other vps online but is not tested. All the needed steps to make it work are described in Install file at the root of this repository.

Note: In my setup, I used a domain name and CloudFlare free account because my home IP address is dynamic. If you don't have a domain name, you can register a free .tk one. CloudFlare is used beause it offers an API to updated the online records and also provides free SSL certificates for domains (SSL is required for amazon integrations).

# Prerequisite

- Raspberry Pi 2 with latest raspbian installed (or any linux server)
- A domain name (free [.tk domain](http://www.dot.tk/en/index.html) can work - not tested -)
- A free [CloudFlare](https://www.cloudflare.com/) account
- Maybe some general linux knowledge?

# Known Issues

- [ ] Next and Previous are not fully functional
- [ ] There are some issues with some videos that don't play and I don't know why, Yet
- [ ] Only video can be played, this is indended and it will not be fixed (no playlist support)
- [ ] Others?

# Currently Implemented
```
Play {search_query}
Search for {search_query}
Play me {search_query}
Listen to {search_query}
Listen {search_query}
```

# How it works

This skill, search youtube for the `{search_query}` on youtube and plays the first video found.

# Thanks to

- [Python pafy](https://github.com/mps-youtube/pafy) - used to get the audio stream from youtube video
- [Youtube-dl](https://github.com/rg3/youtube-dl/) - used with pafy to get youtube information
- [Flask](https://github.com/pallets/flask) - used to serve this application
- [Flask-Ask](https://github.com/johnwheeler/flask-ask) - used for mapping alexa requests
- [uWsgi](https://github.com/unbit/uwsgi) & [nginx](http://nginx.org/) - both used to host the flask application
