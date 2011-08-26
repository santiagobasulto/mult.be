"""
LooLu is Copyright (c) 2009 Shannon Johnson, http://loo.lu/

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import math

class URLHash(object):
    codeset  = "FdwxytrvXaBMS9zp7CQg3EoeGuOKkWLqiAZ85UTRPHIm26Dj4JnbYNhcfVs"
    base = 59 # len(codeset)

    def __init__(self, codeset=None):
        if codeset != None:
            self.codeset = codeset
        self.base = len(self.codeset)

    def largo(self):
        print len(self.codeset)
    
    def encode(self, id):
        if id == 0:
            return self.codeset[0]
        hash = ""

        while (id > 0):
            hash = self.codeset[int(id % self.base)] + hash
            id = math.floor(id / self.base)

        return hash

    def decode(self, encoded):
        id = 0

        for index, char in enumerate(encoded[::-1]):
            n = self.codeset.find(char)

            if n == -1:
                return 0 # Invalid hash

            id += n * math.pow(self.base, index)

        return int(id)

