#!/usr/bin/env python
import argparse
from configparser import SafeConfigParser
from contextlib import closing
from os.path import basename, dirname, join, normpath, realpath
import sys
from urllib2 import urlopen

def generic_open(arg):
    try:
        return urlopen(arg), None
    except ValueError:
        arg = normpath(realpath(arg))
        return open(arg, "r"), dirname(arg)

def playlist_files(config):
    n = config.getint("playlist", "NumberOfEntries")
    for i in xrange(1, n+1):
        yield config.get("playlist", "File%d" % i)

parser = argparse.ArgumentParser(description = "dfsdfsdf")
parser.add_argument("--mpc", dest = "mpc", action = "store_const", const = True, default = False)
parser.add_argument("paths", metavar = "path-or-URL", nargs = "+")
args = parser.parse_args()

config = SafeConfigParser()
for path in args.paths:
    raw_handle, directory = generic_open(path)
    with closing(raw_handle) as handle:
        try:
            config.readfp(handle)
            for raw_fn in playlist_files(config):
                fn = join(directory, raw_fn) if directory != None else raw_fn
                if args.mpc and directory != None:
                    fn = "file://" + fn
                print fn
        except Exception, e:
            print >> sys.stderr, "%s\n    [%s] %s" % (path, type(e).__name__, e)
