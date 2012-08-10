from ConfigParser import SafeConfigParser
from contextlib import closing
from os.path import dirname, join
import sys
from urllib2 import urlopen

def generic_open(arg):
    try:
        return urlopen(arg), None
    except ValueError:
        return open(arg, "r"), dirname(arg)

def playlist_files(config):
    n = config.getint("playlist", "NumberOfEntries")
    for i in xrange(1, n+1):
        yield config.get("playlist", "File%d" % i)

if len(sys.argv) > 1:
    config = SafeConfigParser()
    for arg in sys.argv[1:]:
        raw_handle, directory = generic_open(arg)
        with closing(raw_handle) as handle:
            try:
                config.readfp(handle)
                for raw_fn in playlist_files(config):
                    fn = "file://" + join(directory, raw_fn) if directory != None else raw_fn
                    print fn
            except Exception, e:
                print >> sys.stderr, "%s\n    [%s] %s" % (arg, type(e).__name__, e)
else:
    print >> sys.stderr, "Usage: %s file-or-url [file-or-url ...]"
    sys.exit(1)