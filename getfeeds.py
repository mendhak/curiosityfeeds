import re
from google.appengine.ext import webapp

class MainHandler(webapp.RequestHandler):
    def get(self):

        self.response.out.write("TEST")


app = webapp.WSGIApplication([('/getfeeds', MainHandler)], debug=True)

def GetImageIDs(htmlFragment):
    imageIds = []

    matches = re.findall("ImageID=(\d+)", htmlFragment, re.IGNORECASE)
    if matches:
        imageIds = [int(match) for match in matches]

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
        date = matches[0]

    return date