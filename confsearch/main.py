#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import argparse
from confsearch import *

parser = argparse.ArgumentParser(description='TUI conference search tool')
parser.add_argument('-v', '--verbose', help='verbose mode', action='store_true',
        default=False)
parser.add_argument('-q', '--query', help='query to execute (e.g., acronym)',
        type=str, action='append', required=True)
parser.add_argument('-y', '--year', help='year (default is current year)',
        type=str, action='append')
args = parser.parse_args()

def main():
    # if args.verbose:
    #   confsearch.verbose = True

    conf_names = args.query
    if args.year == None:
        from datetime import datetime as dt
        current = dt.now().year
        conf_years = [str(current), str(current + 1), ]
    else:
        conf_years = []
        for year in args.year:
            if year.startswith('20'):
                conf_years.append(year)
            else:
                conf_years.append('20' + year)

    confarr = []
    for name in conf_names:
        for year in conf_years:
            for c in confobj_generator(name, year):
                if c:
                    confarr.append(c)

    newarr = sorted(confarr, reverse=True)
    for conf in newarr:
        # print "[%s]'[%s]" % (conf.aka, conf.year)
        confinfo(conf)

if __name__ == '__main__':
    main()

