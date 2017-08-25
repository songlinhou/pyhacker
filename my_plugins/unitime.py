import urllib2
from datetime import datetime
def getOnlineUTCTime():
    webpage = urllib2.urlopen("http://just-the-time.appspot.com/")
    internettime = webpage.read()
    OnlineUTCTime = datetime.strptime(internettime.strip(), '%Y-%m-%d %H:%M:%S')
    return OnlineUTCTime
