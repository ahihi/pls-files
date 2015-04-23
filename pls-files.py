#!/usr/bin/env python
import argparse
from configparser import ConfigParser
from contextlib import closing
from os.path import dirname, join, normpath, realpath
import re
import sys
from urllib2 import urlopen

DEFAULT_ENCODINGS = "utf-8,iso-8859-1"
URL_RE = re.compile(r"^[a-z0-9+.-]+:", re.IGNORECASE)

def read_pls(path):
    if path == "-":
        return sys.stdin.read(), None
    else:
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

parser = argparse.ArgumentParser(description = "Print the playlist items in .pls files.")
parser.add_argument("--mpc",
    dest = "mpc",
    action = "store_const",
    const = True,
    default = False,
    help = "print items in a format compatible with `mpc add`")
parser.add_argument("--encoding",
    dest = "encodings",
    metavar = "encoding1,encoding2,...",
    action = "store",
    default = DEFAULT_ENCODINGS,
    help = "character encodings to try (default: %s)" % DEFAULT_ENCODINGS)
parser.add_argument("paths",
    metavar = "path-or-URL",
    nargs = "+",
    help = "file system path or URL to a .pls file")
args = parser.parse_args()

encodings = args.encodings.split(",")

config = ConfigParser()
stdin_data = None
for path in args.paths:
    try:
        if path == "-":
            if stdin_data == None:
                stdin_data = read_pls(path)
            pls_bytes, directory = stdin_data
        else:
            pls_bytes, directory = read_pls(path)

        pls = decode(pls_bytes)
        if pls != None:
            config.read_string(pls)
            for raw_fn in playlist_files(config):
                is_fspath = not URL_RE.match(raw_fn)
                has_dir = directory != None
                fn = join(directory, raw_fn) if is_fspath and has_dir else raw_fn
                if args.mpc and directory != None:
                    fn = "file://" + fn
                print fn
        else:
            print >> sys.stderr, "%s\n    Failed to decode file (tried %s)" % (path, ", ".join(encodings))
    except Exception, e:
        print >> sys.stderr, "%s\n    [%s] %s" % (path, type(e).__name__, e)
