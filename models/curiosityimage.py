from google.appengine.ext import db

class CuriosityImage(db.Model):
    imageid = db.IntegerProperty(default=0)
    title = db.StringProperty()
    description = db.TextProperty()
    date = db.DateProperty()
    imageurl = db.StringProperty()
