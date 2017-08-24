import urllib2
import urllib
from BeautifulSoup import BeautifulSoup
from subprocess import call
import os
import taghelper

#allUrls = ["http://www.npr.org/programs/all-things-considered/2017/08/15/543587917?showDate=2017-08-15"]

def fetchList(manyURLs, scrapedTitle="All Things Considered"):
    for URL in manyURLs:
        fetchATC(URL, scrapedTitle)

def fetchATC(testUrl, scrapedTitle="All Things Considered"):
    response = urllib2.urlopen(testUrl)
    html = response.read()

    soup = BeautifulSoup(html)
    content = soup.findAll("li",{"class":"audio-tool audio-tool-download"})

    counter = 1

    if os.path.isdir("temp") == False:
        print "No temp directory; making one now"
        os.mkdir("temp")
    else:
        print "Temp directory found"

    for i in content:
            foundURL = i.a["href"]
            #print foundURL

            programDate = foundURL.split('/')[-1][:9]
            segment = str(counter).zfill(3)
            filename = foundURL.split('/')[-1][9:-5].split('?')[0]
            savename = programDate + segment + '_' + filename
            print "Saving segment:", savename
            urllib.urlretrieve (i.a["href"], "temp/" + savename)
            counter += 1

    if counter > 1:
        print
        print "Segments found:", counter
        concatName = programDate + "complete_" + scrapedTitle.replace(' ','-') + ".mp3"
        concatNameCruft =  programDate + "complete_" + scrapedTitle.replace(' ','-') + "_MP3WRAP.mp3"
        try:
            print "Concatenating segments..."
            call("mp3wrap " + concatName + " ./temp/*.mp3", shell=True)
        except:
            print "ERROR: Could not concatenate downloaded MP3 files"
            print "Downloaded files are found in the ./temp directory"
        else:
            print "Success!"
            print "Deleting temporary segments..."
            try:
                for file in os.listdir("temp"):
                    if file.endswith(".mp3"):
                        os.remove("temp/" + file)
            except:
                print "Can't remove temp files for some reason"
            else:
                print "Success!"
        try:
            print "Renaming files to remove MP3WRAP cruft..."
            os.rename(concatNameCruft, concatName)
        except:
            print "Error: Cannot rename the crufty filename (should end in _MP3WRAP)"
        else:
            print "Success!"
        try:
            print "Writing MP3 tag info..."
            titleDate = programDate[4:6] + "/" + programDate[6:8] + "/" + programDate[0:4]
            #print titleDate
            title=unicode(titleDate + " " + scrapedTitle)
            print "Title:",title
            artist=unicode(scrapedTitle)
            print "Artist:",artist
            titleDate = programDate[4:2] + "/" + programDate[6:2] + "/" + programDate[0:4]
            taghelper.overwritetag(
                concatName,
                title=title,
                artist=artist
                album=artist
                )
        except:
            print "Error, cannot write MP3 tag"
        else:
            print "Success!"
            print
