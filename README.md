Mult.be
===============

Changelog
---------

###V0.1
* Repo initialized


What is this?
-------------

It's just a simple multiple URL shortener built on top of
[FlaskEngine](https://github.com/zachwill/flask-engine) and
[Google App Engine](http://appengine.google.com/).

The code is really easy to read. The main challenge i've found
building it was to implement a distributed "autoincrement" subsystem.

You may want to take a look at it. It's located at:
/libs/url_shortener/ShardGenerator.py


Useful Commands
---------------

### Setup

    git clone https://github.com/zachwill/flask-engine.git <your_app_name_here>

### Run

    dev_appserver.py .

### Deploy

    appcfg.py update .

### Test

Tests are written using GAE v1.4.3's `testbed` functionality. Currently, [there
is a known bug](http://goo.gl/tDQTz) for users without `PIL` installed.

    python test.py

### Remote Console

    python appengine_console.py multbe


Todo
----
* Improve names (i know ShardGenerator is not a good name at all!)
* Check concurrency safety in ShardGenerator
* Indexes
* add more tests
* add pep8.py to libs
  * create PEP8 TestCase, too


License
-------

**Author**: Santiago Basulto

The code is released under [the GPLv2](http://www.opensource.org/licenses/gpl-2.0.php) license for personal use only.

It can't be used for commercial use. i.e: If you make money with it. Why? Becouse it's for learning purposes.