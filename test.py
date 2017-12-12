#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from confsearch import *

year = 2018
name = 'mobisys'
confsearch.verbose = True

for c in confobj_generator(name, year):
    confinfo(c)
