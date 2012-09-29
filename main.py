from google.appengine.ext import webapp
from curiosityimage import CuriosityImage


class MainHandler(webapp.RequestHandler):
    def get(self):
        ci = CuriosityImage(key_name=str(42))
        ci.imageid = 42
        ci.date = '09.27.2012'
        ci.description = 'DESC1234'
        ci.put()

        ci2 = CuriosityImage(key_name=str(43))
        ci2.imageid = 43
        ci2.description = '2DESC22342'
        ci2.put()

        self.response.out.write(
                '<b>%s</b> wrote:' % ci.description)



app = webapp.WSGIApplication([('/', MainHandler)], debug=True)

