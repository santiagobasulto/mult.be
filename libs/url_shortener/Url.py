'''
Created on 21/06/2011

@author: santiago
'''
import urlparse
import re

class UrlFormater:
    def __init__(self,url,default_protocol='http'):
        if not urlparse.urlsplit(url).scheme:
            url = default_protocol+"://"+url
        self.parts = None
        if is_valid(url):
            self.parts = urlparse.urlsplit(url)
            self.__parse() 
    
    def __parse(self):
        if not self.parts:
            return None
        self.protocol = self.parts.scheme
        self.hostname=self.parts.netloc
        self.querystring = self.parts.path+self.parts.query
        self.port=self.parts.port
    
    def __unicode__(self):
        return self.__str__()
    
    def __str__(self):
        return self.protocol+"://"+self.hostname+self.querystring
    
def is_valid(url):
    p = re.compile('^(https?|ftp)://[a-z0-9-]+(\.[a-z0-9-]+)+([/?].+)?$')
    m = p.match(url)
    if m:
        return True
    return False