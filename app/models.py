"""
Python Datastore API: http://code.google.com/appengine/docs/python/datastore/
"""

from google.appengine.ext import db


class Url(db.Model):
    protocol = db.StringProperty(multiline=False)
    hostname = db.StringProperty(multiline=False)
    querystring = db.StringProperty(multiline=False)
    port = db.StringProperty(multiline=False)


class Short(db.Model):
    hash_value = db.StringProperty(multiline=False)
    created = db.DateTimeProperty(auto_now_add=True)
    ip = db.StringProperty(multiline=False)

class Employee(db.Model):
    first_name = db.StringProperty()
    list = db.ListProperty(db.Key)