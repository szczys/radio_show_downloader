import urllib2
import urllib
from BeautifulSoup import BeautifulSoup
import os
import taghelper
from pydub import AudioSegment   #sudo pip install pydub

#allUrls = ["http://www.npr.org/programs/all-things-considered/2017/08/15/543587917?showDate=2017-08-15"]

def fetchList(manyURLs, scrapedTitle="All Things Considered"):
    for URL in manyURLs:
        fetchATC(URL, scrapedTitle)

def fetchATC(episodeURL, scrapedTitle="All Things Considered"):
    thisProgram = NprProgram(episodeURL, scrapedTitle)    

    counter = 1

    if os.path.isdir("temp") == False:
        print "No temp directory; making one now"
        os.mkdir("temp")
    else:
        print "Temp directory found"

    segmentFiles = []
    for downloadLink in thisProgram.segmentURLs:

            segment = str(thisProgram.segmentURLs.index(downloadLink)).zfill(3)
            filename = thisProgram.getFilename(downloadLink)
            savename = thisProgram.programDate + segment + '_' + filename
            
            print "Saving segment:", savename
            urllib.urlretrieve(downloadLink, "temp/" + savename)
            segmentFiles.append("temp/" + savename)

    segs = thisProgram.countSegments()
    if segs > 1:
        print
        print "Segments found:", segs
        concatName = thisProgram.programDate + "complete_" + thisProgram.showTitle.replace(' ','-') + ".mp3"
        concatNameCruft =  thisProgram.programDate + "complete_" + thisProgram.showTitle.replace(' ','-') + "_MP3WRAP.mp3"
        try:
            print "Concatenating segments..."
            concatenateMP3(segmentFiles, concatName)
        except:
            print "ERROR: Could not concatenate downloaded MP3 files"
            print "Downloaded files are found in the ./temp directory"
            return
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
            print "Writing MP3 tag info..."
            fixMp3Tag(concatName,thisProgram)
        except:
            print "Error, cannot write MP3 tag"
        else:
            print "Success!"
            print

def concatenateMP3(fileList,newFilename):
    fileList.sort()
    
    oneMp3File = AudioSegment.from_mp3(fileList[0])

    if len(fileList) > 1:
        for mp3 in fileList[1:]:
            print ".",
            oneMp3File += AudioSegment.from_mp3(mp3)

    oneMp3File.export(newFilename)
    
def fixMp3Tag(filename,thisProgram):
    titleDate = thisProgram.programDate[4:6] + "/" + thisProgram.programDate[6:8] + "/" + thisProgram.programDate[0:4]
    #print titleDate
    title=unicode(titleDate + " " + thisProgram.showTitle)
    print "Title:",title
    artist=unicode(thisProgram.showTitle)
    print "Artist:",artist
    taghelper.overwritetag(
        filename,
        title=title,
        artist=artist,
        album=artist #Need album for proper threading on Google Play Music app
        )

class NprProgram:
    def __init__(self, episodeURL, showTitle="All Things Considered"):
        self.episodeURL = episodeURL
        self.showTitle = showTitle
        
        response = urllib2.urlopen(episodeURL)
        html = response.read()

        soup = BeautifulSoup(html)
        
        #Historically these classes have changed a few times
        content = soup.findAll("li",{"class":"audio-tool audio-tool-download"})

        self.segmentURLs = []
        for i in content:
            self.segmentURLs.append(i.a["href"])

        #Historically this dated file format has not changed
        self.programDate = self.segmentURLs[0].split('/')[-1][:9]

    def countSegments(self):
        return len(self.segmentURLs)

    def getFilename(self, downloadURL):
        return downloadURL.split('/')[-1][9:-5].split('?')[0]
