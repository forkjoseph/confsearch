#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import argparse
from confsearch import *

parser = argparse.ArgumentParser(description='TUI conference search tool')
parser.add_argument('-q', '--query', help='query to execute (e.g., acronym)',
        required=True, type=str)
parser.add_argument('-y', '--year', help='year (default is current year)', type=str)
parser.add_argument('-v', '--verbose', help='verbose mode', action='store_true',
        default=False)
args = parser.parse_args()

def main():
    if args.year == None:
        from datetime import datetime as dt
        conf_year = [str(dt.now().year), str(dt.now().year + 1)]
        # conf_year = ''
    else:
        if args.year.startswith('20'):
            conf_year = [args.year]
        else:
            conf_year = ['20' + args.year ]

    if args.verbose:
      confsearch.verbose = True

    conf_name = args.query

    confarr = []
    for year in conf_year:
        for c in confobj_generator(conf_name, year):
            confarr.append(c)

    newarr = sorted(confarr, reverse=True)
    for conf in newarr:
        # print "[%s]'[%s]" % (conf.aka, conf.year)
        confinfo(conf)

if __name__ == '__main__':
    main()

