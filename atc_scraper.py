import urllib.request		#pip3 install --user urllib.request
from bs4 import BeautifulSoup	#pip3 install --user bs4
import os
import taghelper
from pydub import AudioSegment	#pipe install --user pydub
import json

#allUrls = ["http://www.npr.org/programs/all-things-considered/2017/08/15/543587917?showDate=2017-08-15"]

temp_dir = "temp/"
output_dir = "files/"

def fetchList(manyURLs, scrapedTitle="All Things Considered"):
    for URL in manyURLs:
        fetchATC(URL, scrapedTitle)

def fetchATC(episodeURL, scrapedTitle="All Things Considered"):
    thisProgram = NprProgram(episodeURL, scrapedTitle)    

    counter = 1

    if os.path.isdir(temp_dir) == False:
        print("No temp directory; making one now")
        os.mkdir(temp_dir)
    else:
        print("Temp directory found")

    if os.path.isdir(output_dir) == False:
        print("No output directory; making one now")
        os.mkdir(output_dir)
    else:
        print("Output directory found")

    segmentFiles = []
    for downloadLink in thisProgram.segmentURLs:

            segment = str(thisProgram.segmentURLs.index(downloadLink)).zfill(3)
            #Insert the segment number into the filename used to save this track
            filename = downloadLink.split('/')[-1]
            underscoreIndex = filename.find('_')
            savename = filename[:underscoreIndex] + '_' + segment + filename[underscoreIndex:]
            
            print("Saving segment:", savename)
            urllib.request.urlretrieve(downloadLink, "temp/" + savename)
            segmentFiles.append("temp/" + savename)

    segs = thisProgram.countSegments()
    if segs > 1:
        print('')
        print("Segments found:", segs)
        concatName = thisProgram.programDate + "_complete_" + thisProgram.showTitle.replace(' ','-') + ".mp3"

        try:
            print("Concatenating segments...")
            concatenateMP3(segmentFiles, output_dir + concatName)
        except:
            print("ERROR: Could not concatenate downloaded MP3 files")
            print("Downloaded files are found in the ./temp directory")
            return
        else:
            print("Success!")
            print("Deleting temporary segments...")
            try:
                for file in os.listdir("temp"):
                    if file.endswith(".mp3"):
                        os.remove("temp/" + file)
            except:
                print("Can't remove temp files for some reason")
            else:
                print("Success!")
        try:
            print("Writing MP3 tag info...")
            fixMp3Tag(output_dir + concatName,thisProgram)
        except:
            print("Error, cannot write MP3 tag")
        else:
            print("Success!")
            print('')

def concatenateMP3(fileList,newFilename):
    fileList.sort()
    
    oneMp3File = AudioSegment.from_mp3(fileList[0])

    if len(fileList) > 1:
        for mp3 in fileList[1:]:
            print(".",end="")
            oneMp3File += AudioSegment.from_mp3(mp3)

    oneMp3File.export(newFilename)
    
def fixMp3Tag(filename,thisProgram):
    datedata = thisProgram.programDate.split('-')
    titleDate = datedata[1] + "/" + datedata[2] + "/" + datedata[0]
    #print(titleDate)
    title=str(titleDate + " " + thisProgram.showTitle)
    print("Title:",title)
    artist=str(thisProgram.showTitle)
    print("Artist:",artist)
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
        
        response = urllib.request.urlopen(episodeURL)
        html = response.read()

        soup = BeautifulSoup(html, "lxml")

        fullshow = soup.find("div",{"id":"full-show"})
        playalljson = json.loads(fullshow.find("b")["data-play-all"])

        self.segmentURLs = list()
        for track in playalljson['audioData']:
            self.segmentURLs.append(track['audioUrl'].split('?')[0])
        
        self.programDate = soup.find("time")['datetime'].strip('-')

    def countSegments(self):
        return len(self.segmentURLs)
