#!/usr/bin/env python3
#
# Quick and dirty public Telegram group message scraper
#
# Usage:
#     python3 tgscrape.py <groupname> [minid] [maxid]
#
# Example:
#     python3 tgscrape.py fun_with_friends 1 1000
#       - dumps messages 1 through 1000 from the group @fun_with_friends
#
# The loop stops when it finds 20 consecutive empty messages

import requests
import sys
from bs4 import BeautifulSoup

def usage(_bin):
    print('Usage: {} <groupname> [minid] [maxid]'.format(_bin))

_argnum = len(sys.argv)

if _argnum < 2:
    usage(sys.argv[0])
    exit()

_minid = 0
_maxid = -1
_groupname = sys.argv[1]
_max404 = 20

if _argnum >= 3:
    _minid = int(sys.argv[2])
    if _argnum >= 4:
        _maxid = int(sys.argv[3])

_url = 'https://t.me/{}/'.format(_groupname)

_id = _minid
_cnt404 = 0
while True:
    _rurl = _url + str(_id) + '?embed=1'
    _output = requests.get(_rurl)
    if _output.status_code < 400:
        _soup = BeautifulSoup(_output.text, 'html.parser')
        _msg = _soup.find('div', class_='tgme_widget_message_text')
        if _msg:
            _author = _soup.find('a', class_='tgme_widget_message_author_name')
            _username = _author['href'].split('/')[3] if _author['href'] else ''
            _datetime = _soup.find('time')['datetime']
            print('[{}] {} (@{}): {}'.format(_datetime, _author.text, _username, _msg.text))
    else:
        _cnt404 += 1
        if _cnt404 == _max404:
            exit()

    if _maxid > 0 and _id == _maxid:
        exit()
    _id += 1

