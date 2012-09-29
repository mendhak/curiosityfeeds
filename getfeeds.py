import re
from google.appengine.ext import webapp

class MainHandler(webapp.RequestHandler):
    def get(self):

        self.response.out.write("TEST")


app = webapp.WSGIApplication([('/getfeeds', MainHandler)], debug=True)

def GetImageIDs(htmlFragment):
    imageIds = []

    if htmlFragment:
        matches = re.findall("ImageID=(\d+)", htmlFragment, re.IGNORECASE)
        if matches:
            imageIds = [int(match) for match in matches]

    return imageIds
