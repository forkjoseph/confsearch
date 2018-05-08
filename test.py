#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
from confsearch import *

year = 2018
# name = 'mobisys'
# confsearch.verbose = True



def help():
    print 'python test.py [FILENAME]'
    sys.exit(0)

if len(sys.argv) < 2:
    help()

with open(sys.argv[1]) as f:
    content = f.readlines()
names = [x.strip() for x in content] 

confs = []
for name in names:
    if '#' in name or '/*' in name:
        continue
    for c in confobj_generator(name, year):
        if not c:
            continue
        confs.append(c)

print 'Sorted by deadlines'
confs = sorted(confs, reverse=True)
for conf in confs:
    # print "[%s]'[%s]" % (conf.aka, conf.year)
    confinfo(conf)
