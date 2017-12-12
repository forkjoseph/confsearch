# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re

__author__ = "HyunJong Joseph Lee"
__copyright__ = "Copyright (C) 2017 " + __author__
__license__ = "GNU GPL v2.0"
__version__ = "0.0.1"

verbose = False

class Conf(object):
    aka_regex = re.compile(r"(.*) (\d{4})")
    date_regex = re.compile(r"(\w{3}) (\d{1,2}), (\d{4})")

    def __init__(self, name, aka):
        self.name = name
        aka = aka.strip()
        tmp = self.aka_regex.search(aka)
        # print tmp.group(1), tmp.group(2)
        self.aka = tmp.group(1).strip()
        self.year = tmp.group(2)

    def __str__(self):
        deadline = self.deadline
        if deadline == 'Jan 1, 1960':
            deadline = 'TBD'
        abstract = self.abstract
        if abstract == 'Jan 1, 1960':
            abstract = 'TBD'
        ret = '{:s} {:s}: {:s}'.format(self.aka, self.year, deadline)
        if self.abstract == '':
            return ret
        ret += ' (abs: {:s})'.format(abstract)
        return ret

    def set_when(self, when):
        if when == '' or when == 'N/A':
            self.when = ''
            return
        start = when.split('-')[0]
        end = when.split('-')[1]

        tmp = self.date_regex.search(start)
        self.when_start_month = tmp.group(1)
        self.when_start_day = tmp.group(2)
        self.when_start_year = tmp.group(3)

        tmp = self.date_regex.search(end)
        self.when_end_month = tmp.group(1)
        self.when_end_day = tmp.group(2)
        self.when_end_year = tmp.group(3)

        self.when = when

    def set_where(self, where):
        if where == '' or where == 'N/A':
            self.where = ''
            return
        self.where = where

    def set_deadline(self, deadline, abstract=''):
        deadline = deadline.strip()
        tmp = self.date_regex.search(deadline)
        if tmp:
            self.deadline_month = tmp.group(1)
            self.deadline_day = tmp.group(2)
            self.deadline_year = tmp.group(3)
            self.deadline = deadline
        else:
            ''' probably TBD '''
            self.deadline_month = ''
            self.deadline_day = ''
            self.deadline_year = ''
            if deadline == 'TBD':
                self.deadline = 'Jan 1, 1960'
            else:
                self.deadline = ''

        abstract = abstract.strip()
        tmp = self.date_regex.search(abstract)
        if tmp:
            self.abstract_month = tmp.group(1)
            self.abstract_day = tmp.group(2)
            self.abstract_year = tmp.group(3)
            self.abstract = abstract
        else:
            self.abstract_month = ''
            self.abstract_day = ''
            self.abstract_year = ''
            if abstract == 'TBD':
                self.abstract = 'Jan 1, 1960'
            else:
                self.abstract = ''

    ''' is it same conference? '''
    def __eq__(self, other):
        return (self.name == other.name and self.year == other.year and
                self.deadline == other.deadline)

    ''' compare deadline! not conference date '''
    def __lt__(self, other):
        from datetime import datetime as dt
        return dt.strptime(self.deadline, '%b %d, %Y') \
                < dt.strptime(other.deadline, '%b %d, %Y')

    def __gt__(self, other):
        from datetime import datetime as dt
        if other.deadline is None:
            print "OTHER:", other
        if self.deadlien is None:
            print "SELF:", self
        return dt.strptime(self.deadline, '%b %d, %Y') \
                > dt.strptime(other.deadline, '%b %d, %Y')
        # return dt(self.deadline_year, self.deadline_month, self.deadline_day) \
        #         > dt(other.deadline_year, other.deadline_month,
        #                 other.deadline_day)

def confinfo(conf):
    ret = '{:s}\'{:s}'.format(conf.aka, conf.year[2:])
    if conf.where != '':
        ret += ', held at {:s}'.format(conf.where)
    if conf.when != '':
        # if conf.when_start_year != conf.when_end_year:
        ret += ', {:s} {:s}-{:s}, {:s}'.format(conf.when_start_month,
                conf.when_start_day, conf.when_end_day, conf.when_start_year)
    ret += '\n\t['
    if conf.deadline != '':
        if conf.deadline == 'Jan 1, 1960':
            ret += 'deadline: TBD'
        else:
            ret += 'deadline: {:s}'.format(conf.deadline)
    if conf.abstract != '':
        ret += ', abs {:s}'.format(conf.abstract)
    ret += ']'
    print ret
    return ret


def confobj_generator(conf_name, conf_year):
    HTTP    = 'http://'
    BASEURL = 'www.wikicfp.com'
    if type(conf_year) == int or type(conf_year) == float:
        conf_year = str(conf_year)

    SEARCHURL = '/cfp/servlet/tool.search?q={:s}&year={:s}'.format(conf_name, conf_year)
    url = HTTP + BASEURL + SEARCHURL 

    if verbose:
        print '{:>10s}:'.format('query'), conf_name
        print '{:>10s}:'.format('year'), conf_year
        print '{:>10s}:'.format('URL'), url
        '''
        curl
        "http://www.wikicfp.com/cfp/servlet/tool.search?q=mobisys&year=2017"  |
        grep -v 'tr>\|Search' | grep '<td.*</td>'
        '''

    r  = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    for div in soup.find_all('table', {'align' : 'center', 'cellpadding' : '2'}):
        confs = div.findAll('tr')
        cnt = 0
        confobj = None
        for conf in confs:
            cnt += 1
            if cnt == 1:
                continue

            ''' contains conf acronym & url '''
            if (cnt % 2) == 0: 
                dates = False
            elif (cnt % 2) == 1:
                dates = True

            if dates is False:
                aka = conf.find('td', {'rowspan' : '2'}).text
                name = conf.find('td', {'colspan' : '3'}).text

                confobj = Conf(name, aka)
                # print aka, ":",
            else:
                orderdetect = 0 # 1 = when, 2 = place, 3 = deadline
                details = conf.findAll('td')
                for detail in details:
                    texts = detail.text.encode('ascii','ignore') 
                    orderdetect += 1
                    if orderdetect == 1:
                        confobj.set_when(texts)
                    elif orderdetect == 2:
                        confobj.set_where(texts)
                    elif orderdetect == 3:
                        deadline = ''
                        abstract = ''
                        if '(' in texts:
                            deadline = texts.split('(')[0]
                            abstract = texts.split('(')[1]
                            abstract = abstract.replace(')', '')
                            # print '%s (abs %s)' % (deadline, abstract)
                        else:
                            deadline = texts
                            # print texts
                        confobj.set_deadline(deadline, abstract)
                        yield confobj


