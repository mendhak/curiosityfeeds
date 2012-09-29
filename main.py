from google.appengine.ext import webapp
from google.appengine.ext import db
import random


class MainHandler(webapp.RequestHandler):
    def get(self):
        greeting = Greeting(parent=greeting_key("222aaa111"))

        greeting.author = str(random.random())

        greeting.content = self.request.get('HTTP_USER_AGENT')
        greeting.put()


        greetings = db.GqlQuery("SELECT * "
                          "FROM Greeting "
                          "WHERE ANCESTOR IS :1 "
                          "ORDER BY date DESC LIMIT 10",
                          greeting_key("222aaa111"))

        for greeting in greetings:
            if greeting.content == self.request.get('HTTP_USER_AGENT'):
                greeting.content = "This was an update!"
                greeting.put()


            self.response.out.write(
                '<b>%s</b> wrote:' % greeting.content)
        self.response.out.write('222Hello world!')


app = webapp.WSGIApplication([('/', MainHandler)],
                             debug=True)

def greeting_key(k):
  """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
  return db.Key.from_path('Greeting', k or 'default_greeting')

class Greeting(db.Model):
    author = db.StringProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)
