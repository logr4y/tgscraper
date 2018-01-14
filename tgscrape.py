#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick and dirty public Telegram group message scraper

Usage:
    $ python3 tgscrape.py <groupname> [minid] [maxid]

Example:
    $ python3 tgscrape.py fun_with_friends 1 1000
        - dumps messages 1 through 1000 from the group @fun_with_friends

The loop stops when it finds 20 consecutive empty messages
"""

import sys
import time
import requests
from bs4 import BeautifulSoup

def usage(pyfile):
    """ Usage """
    return 'Usage: {} <groupname> [minid] [maxid]'.format(pyfile)

def get_sender(obj):
    """ Retrieves the sender of a message """
    obj = obj.find('div', class_='tgme_widget_message_author')
    author = list(obj.children)[0]
    return_name = author.text
    if author.name == 'a':
        return_username = author['href'].split('/')[3]
    elif author.name == 'span':
        return_username = ''
    else:
        exit("author retrieve error")

    return (return_name, return_username)

argnum = len(sys.argv)

if argnum < 2:
    exit(usage(sys.argv[0]))

min_id = int(sys.argv[2]) if argnum >= 3 else 0
max_id = int(sys.argv[3]) if argnum >= 4 else -1
groupname = sys.argv[1]
max_err = 20

url = 'https://t.me/{}/'.format(groupname)

msg_id = min_id
cnt_err = 0
while True:
    r_url = url + str(msg_id) + '?embed=1'
    response = requests.get(r_url)
    if len(response.text) > 3000:
        soup = BeautifulSoup(response.text, 'html.parser')
        msg = soup.find_all('div', class_='tgme_widget_message_text')
        if msg:
            if len(msg) == 2:
                quote = msg[0].text
                msg = msg[1]
            else:
                msg = msg[0]
                quote = ''
            (name, username) = get_sender(soup)
            datetime = soup.find('time')['datetime']
            print(
                '[{}] {}{} {}{}'.format(datetime,
                                      name,
                                      ' (@{}):'.format(username) if username else ':',
                                      '{{ {} }} '.format(quote) if quote else '',
                                      msg.text))
    else:
        cnt_err += 1
        if cnt_err == max_err:
            exit('{} consecutive empty messages. Exiting...'.format(max_err))

    if msg_id == max_id:
        exit('All messages retrieved. Exiting...')

    msg_id += 1
    time.sleep(0.5)
