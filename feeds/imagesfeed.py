from google.appengine.ext import webapp
import time
from feeds import getfeeds
from models.curiosityimage import CuriosityImage
from email import utils


class ImagesFeed(webapp.RequestHandler):
    def get(self):

        self.response.headers['Content-Type'] = "application/rss+xml"

        maxImages = 50

        if self.request.get('all'):
            maxImages = 100000

        q = CuriosityImage.all()
        q.order('-date')

        self.response.out.write("<?xml version=\"1.0\"?>\r\n")
        self.response.out.write("<rss version=\"2.0\" xmlns:dc=\"http://purl.org/dc/elements/1.1/\">\r\n")
        self.response.out.write("<channel>\r\n")
        self.response.out.write("<title>MSL Curiosity Images</title>\r\n")
        self.response.out.write("<link>http://mars.jpl.nasa.gov/msl/multimedia/images/</link>\r\n")
        self.response.out.write("<description>MSL Curiosity Images</description>\r\n")
        self.response.out.write("<language>en-us</language>\r\n")

        for p in q.run(limit=maxImages):
            self.response.out.write("<item>\r\n")
            self.response.out.write("<title><![CDATA[" + p.title + "]]></title>\r\n")
            self.response.out.write("<link>" + getfeeds.GetImagePageUrl(p.imageid) + "</link>\r\n")
            self.response.out.write("<description><![CDATA[<p class=\"image-container\" style=\"text-align: center;\">")
            self.response.out.write("<img src=\"" + p.imageurl + "\" alt=\"" + p.title + "\" />")
            self.response.out.write("</p>")

            self.response.out.write(p.description)
            self.response.out.write("]]></description>\r\n")

            dttuple = p.date.timetuple()
            timestamp = time.mktime(dttuple)
            self.response.out.write("<pubDate>" + utils.formatdate(timestamp) + "</pubDate>")

            self.response.out.write("</item>\r\n")





app = webapp.WSGIApplication([('/images', ImagesFeed)], debug=True)

