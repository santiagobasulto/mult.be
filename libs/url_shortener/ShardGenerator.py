'''
Created on 23/08/2011

@author: santiago
'''
from google.appengine.ext import db
from random import randint

class ShardGeneratorException(Exception): pass
class NegativeStartException(ShardGeneratorException): pass

class ShardCounterGenerator(db.Model):
    start = db.IntegerProperty(required=True)
    length = db.IntegerProperty(default=1000,required=True)
    current = db.IntegerProperty(required=True,default=1)
    
    def next(self):
        if (self.current>self.length):
            return None
        i = self.start+self.current
        self.current +=1
        #db.put_async(self)
        self.put()
        return i
    
    def hasNext(self):
        return self.current<=self.length    


class ShardGeneratorWrapper(db.Model):
    last_start = db.IntegerProperty(required=True,default=0)
    default_length = db.IntegerProperty(required=True,default=10000)
    shards = db.ListProperty(db.Key)
    shard_count = 30
    
    def next(self):
        next = None
        index = randint(0,self.shard_count-1)
        if index < len(self.shards):
            key = self.shards[index]
            shard = db.get(key)
            next = shard.next()
            if next is not None:
                return next
            else:
                #TODO
                return self.newShard(index).next()
        return self.newShard().next()
    
    def newShard(self,position=None):
        new_shard = ShardCounterGenerator(start=self.last_start,length=self.default_length)
        key = new_shard.put()
        self.last_start += self.default_length
        if position is None:
            self.shards.append(key)
        else:
            self.shards.pop(position)
            self.shards.insert(position,key)
        #db.put_async(self)
        self.put()
        return new_shard
    
class ShardGeneratorFacade():
    key_name = "shard_generator_factory_1"
    
    def __init__(self):
        self.wrapper = ShardGeneratorWrapper.get_by_key_name(self.key_name)
        if self.wrapper is None:
            self.wrapper = ShardGeneratorWrapper(key_name = self.key_name)
            self.wrapper.shards = []
            self.wrapper.put()
    
    def next(self):
        return self.wrapper.next()