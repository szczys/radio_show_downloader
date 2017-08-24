import eyed3    #sudo apt-get install python-eyed3

myMP3 = '/home/mike/Downloads/cartalk/Car_Talk_2011-10-15.mp3'

def showtag(filename):
    audiofile = eyed3.load(filename)
    print "Title:", audiofile.tag.title
    print "Artist:", audiofile.tag.artist
    print "Album:", audiofile.tag.album
    print "Album Artist:", audiofile.tag.album_artist
    print "Track Number:", audiofile.tag.track_num

def overwritetag(filename, title=None, artist=None, album=None, album_artist=None, tracknum=None):
    audiofile = eyed3.load(filename)
    audiofile.tag.title = title
    audiofile.tag.artist = artist
    audiofile.tag.album = album
    audiofile.tag.album_artist = album_artist
    audiofile.tag.track_num = tracknum
    audiofile.tag.save()
