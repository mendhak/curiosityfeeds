from google.appengine.ext import webapp


class MainHandler(webapp.RequestHandler):
    def get(self):

        url = self.request.get('url')


        self.response.out.write(
                'Placeholder')



app = webapp.WSGIApplication([('/', MainHandler)], debug=True)

