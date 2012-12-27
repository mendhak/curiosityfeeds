from google.appengine.ext import webapp


class MainHandler(webapp.RequestHandler):
    def get(self):

#        url = self.request.get('url')


#        self.response.out.write(
#                'You can subscribe to the <a href=\"/images\">MSL Curiosity Image feed here</a>.')

        self.redirect('/images')



app = webapp.WSGIApplication([('/', MainHandler)], debug=True)

