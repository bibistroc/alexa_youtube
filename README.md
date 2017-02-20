[![codecov](https://codecov.io/gh/bibistroc/alexa_youtube/branch/master/graph/badge.svg)](https://codecov.io/gh/bibistroc/alexa_youtube) [![Build Status](https://travis-ci.org/bibistroc/alexa_youtube.svg?branch=master)](https://travis-ci.org/bibistroc/alexa_youtube)

# Echo Dot Youtube Skill

This skill is intented for personal use only (in development mode), is higly reccomended to not push it on amazon marketplace.

# Information

I wrote and tested this code on a Raspberry Pi 2 b+ model. It should also work an Raspberry Pi 3 on any other vps online but is not tested. All the needed steps to make it work are described below.

Note: In my setup, I used a domain name and CloudFlare free account because my home IP address is dynamic. If you don't have a domain name, you can register a free .tk one. CloudFlare is used beause it offers an API to updated the online records and also provides free SSL certificates for domains (SSL is required for amazon integrations).

# Prerequisite

- Raspberry Pi 2 with latests raspbian installed (or any linux server)
- A domain name (free [.tk domain](http://www.dot.tk/en/index.html) can work - not tested -)
- A free [CloudFlare](https://www.cloudflare.com/) account
- Maybe some general linux knowledge?

# Install

## Raspberry Pi install prerequisites

Install python, git & build-essential (build-essential is used for pip packages build)
```sh
sudo apt-get install python python-dev python-pip python-virtualenv git build-essential
```
Install requested libraries for pip
```sh
sudo apt-get install libffi-dev libssl-dev libav-tools
```
Install nginx & uWSGI which will be used to serve the python app
```sh
apt-get install nginx uwsgi uwsgi-plugin-python
```
Create a directory for the app (example: /home/pi/alexa_youtube)
```sh
mkdir /home/pi/alexa_youtube
# & change to that directory
cd /home/pi/alexa_youtube
```
Clone this repo in that directory (don't forget the last "." from this command to avoid creating a new directory)
```sh
git clone <repo_url> .
```
Go to [Google Developers console](https://console.developers.google.com/apis/credentials) and create a new app there (give it any name you like it doesn't matter). On the newly created app, go to `credentials` page and generate `Api Key` credentials. Copy the generated api key and paste it into `alexa/config.ini` file as the `api_key`
```sh
# open the file with pico and replace <api_key> with your api_key and <domain_name> with your domain
# for example, if you domain is example.com, replace <domain_name> with https://example.com
pico alexa/config.ini
# press ctrl + x, y and enter to save and close pico
```

Install python requirements and wait for this to finish. This could take a long time
```sh
pip install -r requirements.txt
```

## Configure uWSGI & nginx
The following commands are runned as `pi` user on the raspberry pi.

### uWsgi Part
```sh
# change directory to uWSGI service
cd /etc/uwsgi/apps-available
# copy the file from helper/uWsgi/alexa.ini into that directory
sudo cp /home/pi/alexa_youtube/helper/uWsgi/alexa.ini ./
# change the file to resemble the location of your app
sudo pico alexa.ini
# change chdir = /home/pi/alexa_youtube
# if is not already this path
# press ctrl + x, y and enter to save and close pico
# create symlink to /etc/uwsgi/apps-enabled
cd ../apps-enabled
sudo ln -s ../apps-available/alexa.ini ./
# restart uWSGI
sudo /etc/init.d/uwsgi restart
```
### Nginx Part
```sh
# change directory to nginx
cd /etc/nginx/sites-available
# copy the file from helper/nginx/alexa into that directory
sudo cp /home/pi/alexa_youtube/helper/nginx/alexa ./
# change the server_name to your own domain
sudo pico alexa
# press ctrl + x, y and enter to save and close pico
# create symlink to /etc/nginx/sites-enabled
cd ../sites-enabled
sudo ln -s ../sites-available/alexa ./
# restart nginx
sudo /etc/init.d/nginx restart
```
If all the steps above are successfully, you can see your application up and running on your custom domain setted in nginx `server_name`

# Amazon Part
In order for this skill to be available in alexa, you need to add it. Login into [Alexa Amazon Developers](https://developer.amazon.com/edw/home.html#/skills/list) website with the same credentials logged on you `echo dot`.

### Skill Information

- From the top right corner on Alexa skills kit page, click on `Add a New Skill`
- Check `Custom Interaction Model` on `Skill Type`
- Set the language to `English (U.S.)`
- Set the `Name` to whatever you want
- `Invocation Name` must be the word that Alexa uses when referes to your skill (if you choose, for example, `Pie` you will need to say to Alexa: `Ask pie to play <song from youtube>`
- Set `Audio Player` to `Yes`

### Interaction Model

- In `Intent Schema` add the content of the file `helper/amazon/intent.json` into the field
- In `Sample Utterances` add the content of the file `helper/amazon/utterance.txt` into the field
- Click `Save`
The interaction model will be build but you can continue with the next step

### Configuration

- Set `HTTPS` for `Service Endpoint Type`
- Choose `Europe` or `North America` which is close to your location
- Add the url of you domain setted in nginx `server_name` config file and append `/alexa` at the end and `https://` before (For example, if your domain is `example.com`, insert `https://example.com/alexa` into the field.
- Set `Account Linking` to `No`

### SSL Certificate

- Choose the second option: `My development endpoint is a sub-domain of a domain that has a wildcard certificate from a certificate authority `

### Publishing Information & Privacy & Compliance

Don`t check enything on this steps, we will not publish this, you are done :)