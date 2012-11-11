#!/usr/bin/env python
import argparse
from configparser import ConfigParser
from contextlib import closing
from os.path import dirname, join, normpath, realpath
import sys
from urllib2 import urlopen

encodings = ("utf-8", "iso-8859-1")

def read_pls(path):
    try:
        with closing(urlopen(path)) as resp:
            return resp.read(), None
    except ValueError:
        the_path = normpath(realpath(path))
        with open(the_path, "r") as fh:
            return fh.read(), dirname(the_path)

def decode(text):
    result = None
    for enc in encodings:
        try:
            result = text.decode(enc)
            break
        except UnicodeDecodeError:
            pass
    return result

def playlist_files(config):
    n = config.getint("playlist", "NumberOfEntries")
    for i in xrange(1, n+1):
        yield config.get("playlist", "File%d" % i)

parser = argparse.ArgumentParser()
parser.add_argument("--mpc", dest = "mpc", action = "store_const", const = True, default = False)
parser.add_argument("--encoding", dest = "encodings", metavar = "encoding1,encoding2,...", action = "store")
parser.add_argument("paths", metavar = "path-or-URL", nargs = "+")
args = parser.parse_args()

if args.encodings != None:
    encodings = args.encodings.split(",")

config = ConfigParser()
for path in args.paths:
    try:
        pls_bytes, directory = read_pls(path)
        pls = decode(pls_bytes)
        if pls != None:
            config.read_string(pls)
            for raw_fn in playlist_files(config):
                fn = join(directory, raw_fn) if directory != None else raw_fn
                if args.mpc and directory != None:
                    fn = "file://" + fn
                print fn
        else:
            print >> sys.stderr, "%s\n    Failed to decode file (tried %s)" % (path, ", ".join(encodings))
    except Exception, e:
        print >> sys.stderr, "%s\n    [%s] %s" % (path, type(e).__name__, e)
