import re
import urllib2
import urlparse
from datetime import datetime
from google.appengine.ext import webapp
from curiosityimage import CuriosityImage

class MainHandler(webapp.RequestHandler):
    def get(self):
        imageIndexPageHTML = urllib2.urlopen('http://mars.jpl.nasa.gov/msl/multimedia/images/').read()
        imageIds = GetImageIDs(imageIndexPageHTML)

        for i,j in imageIds[0:2]:
            imagePageHtml = urllib2.urlopen(GetImagePageUrl(i)).read()
            ci = CuriosityImage(key_name=str(i))
            ci.imageid = i
            ci.title = GetImageTitle(imagePageHtml)
            ci.description = GetImageDescription(imagePageHtml)
            ci.date = GetImageDate(imagePageHtml)
            ci.imageurl = GetMediumImageUrl(imagePageHtml)
            ci.put()
            #SaveCuriosityImage(ci)


        self.response.out.write("TEST")


app = webapp.WSGIApplication([('/getfeeds', MainHandler)], debug=True)

def GetImageIDs(htmlFragment):
    imageIds = []

    for m in re.finditer("ImageID=(\d+)", htmlFragment, re.IGNORECASE):
        thumbPosition = htmlFragment.find("src=", m.start()) + 5
        thumbEndPosition = htmlFragment.find("\"", thumbPosition)
        thumbNail = htmlFragment[thumbPosition : thumbEndPosition]
        thumbNail = urlparse.urljoin('http://mars.jpl.nasa.gov/msl/multimedia/images/', thumbNail)
        imageIds.append((int(m.group(1)),thumbNail))

    return imageIds


def GetImageTitle(htmlFragment):
    title = ''
    matches = re.findall("<strong>([^<]+)</strong>", htmlFragment, re.IGNORECASE)
    if matches:
        title = matches[0]

    return title


def GetImageDate(htmlFragment):
    date = ''
    matches = re.findall("(\d{2}\.\d{2}\.\d{4})", htmlFragment, re.IGNORECASE)
    if matches:
        dateString = matches[0]
        date = (datetime.strptime(dateString, '%m.%d.%Y')).date()
    return date


def GetImageTitlePosition(htmlFragment):
    position = None
    matches = re.search("<strong>([^<]+)</strong>", htmlFragment, re.IGNORECASE)
    if matches:
        position = matches.start()

    return position


def GetImageDescription(htmlFragment):
    desc = ''

    titlePosition = GetImageTitlePosition(htmlFragment)

    if titlePosition:
        tdPosition = htmlFragment.find("<td>", titlePosition)
        closingTdPosition = htmlFragment.find("</td>", tdPosition)
        desc = htmlFragment[tdPosition+4 :closingTdPosition]
        #Removes whitespace
        desc = ' '.join(desc.split())

    return desc

def GetMediumImageUrl(htmlFragment):
    imgSrc = ''
    titlePosition = GetImageTitlePosition(htmlFragment)

    if titlePosition:
        imgPosition = htmlFragment.rfind("href=\"", 0, titlePosition) + 6
        imgEndPosition = htmlFragment.find("\"", imgPosition)
        imgSrc = htmlFragment[imgPosition : imgEndPosition]
        imgSrc = urlparse.urljoin('http://mars.jpl.nasa.gov/msl/multimedia/images/', imgSrc)
    return imgSrc


def SaveCuriosityImage(curiosityImage):
    dbCI = CuriosityImage.get_by_key_name(curiosityImage.key().name())

    if dbCI:
        dbCI.__dict__.update(curiosityImage.__dict__)
    else:
        dbCI = curiosityImage

    dbCI.put()


def GetImagePageUrl(imageId):
    return 'http://mars.jpl.nasa.gov/msl/multimedia/images/?ImageID=' + str(imageId)