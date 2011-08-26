"""
Flask Module Docs:  http://flask.pocoo.org/docs/api/#flask.Module

This file is used for both the routing and logic of your
application.

Author: Santiago Basulto
"""

from flask import Module, url_for, render_template, request, redirect
from models import Short,Url

from google.appengine.ext import db

from url_shortener import ShardGenerator
from url_shortener.Url import UrlFormater 
from url_shortener.hash import URLHash
import url_shortener

from google.appengine.ext import db
        
views = Module(__name__, 'views')

class Mock(db.Model):
    data = db.StringProperty()

@views.route('/test')
def test():
    resp = ""
    url = UrlFormater("http://google.com")
    return str(url)
    return resp

@views.route('/')
def index():
    """Render website's index page."""
    return render_template('index.html')

@views.route('/qunit/')
def qunit():
    """Render a QUnit page for JavaScript tests."""
    return render_template('test_js.html')


@views.after_request
def add_header(response):
    """Add header to force latest IE rendering engine and Chrome Frame."""
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    return response


@views.app_errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


@views.route('/<hash>')
def display_shortened_urls(hash):
    #if the hash is not there
    q = db.Query(Short)
    q.filter("hash_value = ",hash)
    short = q.get()
    if not short:
        return render_template('404.html'), 404
    urls = Url.gql("WHERE ANCESTOR IS :1", short)
    return render_template('hash.html',urls=urls)

@views.route("/shorten/", methods=["POST","GET"])
def shorten():
    if not request.method == 'POST':
        return redirect(url_for('index'))
    urls= request.form.getlist('urls')
    
    urls = list(set(urls))
    if len(urls) > 25:
        urls = urls [:25]
        
    sanitized_urls= [UrlFormater(url) for url in urls if url_shortener.Url.is_valid(url)]
    if len(sanitized_urls)<=0:
        return redirect(url_for('index'))
    
    id_generator = ShardGenerator.ShardGeneratorFacade()
    id = id_generator.next()
    short_key = db.Key.from_path('Short',id)
    #Get the Short
    s = Short(key=short_key)
    #Calculate its hash
    s.hash_value = URLHash().encode(id)
    s.put()
    us = []
    for url in sanitized_urls:
        u = Url(protocol= url.protocol, hostname=url.hostname,querystring=url.querystring,port=url.port,parent = s)
        us.append(u)
    db.put(us)
    
    return render_template('shorten.html',hash=s.hash_value)