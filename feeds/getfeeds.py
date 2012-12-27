import re
import urlparse
import logging
from datetime import datetime
from time import sleep
from google.appengine.api import urlfetch
from google.appengine.ext import webapp
import sys
from models.curiosityimage import CuriosityImage
from google.appengine.api import memcache



class MainHandler(webapp.RequestHandler):

    def log(self, message):
        self.response.out.write("<br />" + message)
        logging.info(message)

    def get(self):
        if self.request.get('firstrun'):
            self.firstRun = True
            self.log("firstRun set to true")

        else:
            self.firstRun = False

        #'http://mars.jpl.nasa.gov/msl/multimedia/images/'
        url = self.request.get('url')

        self.ParseAllPagesAndFollowNextLink(url)
        self.response.out.write("<br />DONE")

    def GetUrlContents(self, url):
        try:
            return urlfetch.fetch(url, deadline=60).content
        except:
            self.log( "Could not get URL:" + url + ". Error: " + str(sys.exc_info()[0]))

    def ParseAllPagesAndFollowNextLink(self, imageIndexPageUrl):

        if imageIndexPageUrl is None or len(imageIndexPageUrl) == 0:
            return

        self.log("Processing %s" % imageIndexPageUrl)

        imageIndexPageHTML = self.GetUrlContents(imageIndexPageUrl)

        if not imageIndexPageHTML:
            self.log("imageIndexPageHTML is empty for " + imageIndexPageUrl)
            return

        imageIds = GetImageIDs(imageIndexPageHTML)

        for i,j in imageIds:
            if CuriosityImageExists(i):
                self.log("Image ID %s already exists in the datastore." % i)
                if not self.firstRun:
                    self.log("Stopping processing.")
                    return
                else:
                    continue

            imagePageHtml = self.GetUrlContents(GetImagePageUrl(i))
            if not imagePageHtml:
                self.log("imagePageHtml is empty for " + str(i))
                break
            ci = CuriosityImage(key_name=str(i))
            ci.imageid = i
            ci.title = GetImageTitle(imagePageHtml)
            ci.description = GetImageDescription(imagePageHtml)
            ci.date = GetImageDate(imagePageHtml)
            ci.imageurl = GetMediumImageUrl(imagePageHtml)
            SaveCuriosityImage(ci)

        self.log("Sleeping for 5 seconds")
        sleep(5)

        #App engine doesn't like long running pages,
        #so we redirect to same page with different querystring
        self.ProcessNextPage(imageIndexPageHTML)


    def ProcessNextPage(self, htmlFragment):
        nextPage = GetNextPageUrl(htmlFragment)
        if nextPage:
            redirectUrl = '/getfeeds?url=' + nextPage
            if self.firstRun:
                redirectUrl += '&firstrun=firstrun'
            self.redirect(redirectUrl)


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
        desc = ReplaceRelativeUrls(desc)
        desc = CleanUpHtml(desc)

    return safe_unicode(desc)

def ReplaceRelativeUrls(desc):

    replacements = []

    for m in re.finditer("\"\.\./",desc):
        closingPos = desc.find("\"", m.start()+1)
        relativeUrl = desc[m.start()+1:closingPos]
        replacements.append((relativeUrl,urlparse.urljoin('http://mars.jpl.nasa.gov/msl/multimedia/images/', relativeUrl)  ))

    for r in replacements:
        desc = desc.replace(r[0], r[1])

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

    if dbCI is None:
        memcache.flush_all()
        curiosityImage.put()


def GetImagePageUrl(imageId):
    return 'http://mars.jpl.nasa.gov/msl/multimedia/images/?ImageID=' + str(imageId)


def CuriosityImageExists(imageId):
    return CuriosityImage.get_by_key_name(str(imageId)) is not None


def GetNextPageUrl(htmlFragment):
    nextSrc = None

    nextPosition = htmlFragment.find("Next &gt;")

    if nextPosition > -1:
        hrefPosition = htmlFragment.rfind("href=\"",0,nextPosition)+6
        hrefEndPosition = htmlFragment.find("\"", hrefPosition)
        nextSrc = htmlFragment[hrefPosition:hrefEndPosition]
        nextSrc = urlparse.urljoin('http://mars.jpl.nasa.gov/msl/multimedia/images/', nextSrc )

    return nextSrc

def safe_unicode(obj, *args):
    """ return the unicode representation of obj """
    try:
        return unicode(obj, *args)
    except UnicodeDecodeError:
        # obj is byte string
        ascii_text = str(obj).encode('string_escape')
        return unicode(ascii_text)

def safe_str(obj):
    """ return the byte string representation of obj """
    try:
        return str(obj)
    except UnicodeEncodeError:
        # obj is unicode
        return unicode(obj).encode('unicode_escape')

def CleanUpHtml(desc):
    """ Replaces bad HTML such as <br> with <br /> """
    desc = desc.replace('<br>','<br />')
    return desc