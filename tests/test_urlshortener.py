import unittest
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext import testbed

from url_shortener.hash import URLHash

from url_shortener import ShardGenerator
from url_shortener.ShardGenerator import ShardCounterGenerator,ShardGeneratorFacade

class URLHashTest(unittest.TestCase):
    hash_conocidos = ( (0,"F"),
                       (1,"d"),
                       (1001,"7V"),
                      )        
    def test_codeset_base_len(self):
        self.assertEquals(URLHash.base,len(URLHash.codeset))

    def test_encode_hash_conocidos(self):
        uHash =URLHash()
        for k,v in self.hash_conocidos:
            self.assertEquals(uHash.encode(k),v)
            
class ShardCounterGeneratorTest(unittest.TestCase):
        
    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        #self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()
        
    def testSimpleShardWorks(self):
        s = ShardCounterGenerator(start=0)
        self.assertEquals(s.next(),1)
    
    def testCounterNoNext(self):
        s = ShardCounterGenerator(start=0,length=1)
        self.assertEquals(1,s.next())
        self.assertFalse(s.hasNext())
        
    def testCounterLimit(self):
        s = ShardCounterGenerator(start=0,length=5)
        for i in range(1,6):
            self.assertEquals(s.next(),i)
        self.assertEquals(s.next(),None)
        
    def testCounterRange(self):
        s1 = ShardCounterGenerator(start=0,length=5)
        s2 = ShardCounterGenerator(start=5,length=5)
        for i in range(1,6):
            self.assertEquals(s1.next(),i)
            self.assertEquals(s2.next(),i+5)
        self.assertEquals(s1.next(),None)
        self.assertEquals(s2.next(),None)
        
class RepeatedNumberException(Exception):pass
class NoneException(Exception):pass

class ShardGeneratorFacadeTest(unittest.TestCase):
    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        #self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()
    """
    def testAll(self):
        big_collection = {}
        gen = ShardGeneratorFacade()
        for i in range(100000):
            n = gen.next()
            if n in big_collection:
                raise RepeatedNumberException("Repetido el siguiente numero: %s"%n)
            if n is None:
                raise NoneException("Encontre un None en: %s"%i)
            big_collection[n] = 0
            if i % 1000==0:
                print "\n feedback: %s" %i

    def testMoreThan20000(self):
        gen = ShardGeneratorFacade()
        for i in range(19999):
            gen.next()
        for i in range(5):
            print gen.next()
    """