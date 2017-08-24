# All Things Considered Scraper

This script is used to download All Things Considered and Morning Edition as one single large MP3 file (normal download is around 20 segments per show).

## Installation:

sudo apt-get install mp3wrap python-eyed3

## Usage:

* Run script in idle
* single show download:
* * fetchATC('http://www.npr.org/programs/all-things-considered/2017/08/22/545198506?showDate=2017-08-22')
* multiple show download:
* * fetchList([url1,url2,etc])
* Download Morning Edition:
* * fetchATC(url,"Morning Edition")
* * fetchList([url1, url2, etc.],"Morning Edition")
