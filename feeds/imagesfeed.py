from google.appengine.ext import webapp
import time
from feeds import getfeeds
from models.curiosityimage import CuriosityImage
from email import utils
from google.appengine.api import memcache


class ImagesFeed(webapp.RequestHandler):
    def get(self):

        self.response.headers['Content-Type'] = "application/rss+xml"

        maxImages = 50

        if self.request.get('all'):
            maxImages = 100000


        finalOutput = memcache.get('Last50Images')

        if not finalOutput or self.request.get('all'):
            requestedImages = self.GetImagesFromDataStore(maxImages)

            rssXml = ["<?xml version=\"1.0\"?>\r\n",
                      "<rss version=\"2.0\" xmlns:dc=\"http://purl.org/dc/elements/1.1/\">\r\n", "<channel>\r\n",
                      "<title>MSL Curiosity Images</title>\r\n",
                      "<link>http://mars.jpl.nasa.gov/msl/multimedia/images/</link>\r\n",
                      "<description>MSL Curiosity Images</description>\r\n", "<language>en-us</language>\r\n"]

            for p in requestedImages:
                rssXml.append("<item>\r\n")
                rssXml.append("<title><![CDATA[" + p.title + "]]></title>\r\n")
                rssXml.append("<link>" + getfeeds.GetImagePageUrl(p.imageid) + "</link>\r\n")
                rssXml.append("<description><![CDATA[<p class=\"image-container\" style=\"text-align: center;\">")
                rssXml.append("<img src=\"" + p.imageurl + "\" alt=\"" + p.title + "\" />")
                rssXml.append("</p>")

                rssXml.append(p.description)
                rssXml.append("]]></description>\r\n")

                dttuple = p.date.timetuple()
                timestamp = time.mktime(dttuple)
                rssXml.append("<pubDate>" + utils.formatdate(timestamp) + "</pubDate>")

                rssXml.append("</item>\r\n")

            rssXml.append("</channel>\r\n")
            rssXml.append("</rss>")

            finalOutput = ''.join(rssXml)

            if not self.request.get('all'):
                memcache.add('Last50Images', finalOutput)


        self.response.out.write(finalOutput)

    def GetImagesFromDataStore(self, numberOfImages):
        q = CuriosityImage.all()
        q.order('-date')
        return q.fetch(limit=numberOfImages)



app = webapp.WSGIApplication([('/images', ImagesFeed)], debug=True)

