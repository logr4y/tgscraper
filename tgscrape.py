#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick and dirty public Telegram group message scraper

Usage:
    $ python3 tgscrape.py <groupname> [minid] [maxid]

Example:
    $ python3 tgscrape.py fun_with_friends 1 1000
        - dumps messages 1 through 1000 from the group @fun_with_friends

The loop stops when it finds 20 consecutive empty messages (defined by max_err in config.py)
"""

import sys
import time
import requests
from bs4 import BeautifulSoup
import config

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
        exit("`author` retrieval error. Exiting...")

    return (return_name, return_username)

def scrape_run(lurl, lmin_id, lmax_id):
    """ Main logic """
    msg_id = lmin_id
    cnt_err = 0
    while True:
        r_url = lurl + str(msg_id) + '?embed=1'
        response = requests.get(r_url)
        if len(response.text) > 3000:
            soup = BeautifulSoup(response.text, 'html.parser')
            datetime = soup.find('time')['datetime']
            if datetime:
                (name, username) = get_sender(soup)
                outputline = '[{}] {}{}: '.format(datetime,
                                        name,
                                        ' (@{})'.format(username) if username else ''
                                        )

                msg = soup.find_all('', class_=config.text_class)
                if msg:
                    if len(msg) == 2:
                        quote = msg[0].text
                        msg = msg[1].text
                    else:
                        msg = msg[0].text
                        quote = ''
                    outputline += '{}{}'.format(
                                            '{{ {} }} '.format(quote) if quote else '',
                                            msg)

                media = soup.find('', class_=config.photo_class) or \
                    soup.find('', class_=config.video_class) or \
                    soup.find('', class_=config.voice_class)

                if media:
                    if media['class'][0] == config.photo_class:
                        outputline += media['style'].split("'")[1]

                    if media['class'][0] == config.video_class:
                        outputline += media.video['src']

                    if media['class'][0] == config.voice_class:
                        outputline += media.audio['src']

                print(outputline)
                outputline = ''

        else:
            cnt_err += 1
            if cnt_err == config.max_err:
                exit('{} consecutive empty messages. Exiting...'.format(config.max_err))

        if msg_id == lmax_id:
            print('All messages retrieved. Exiting...')
            exit(0)

        msg_id += 1
        time.sleep(config.sleeptime)


if __name__ == '__main__':
    try:
        argnum = len(sys.argv)

        if argnum < 2:
            exit(usage(sys.argv[0]))

        url = 'https://t.me/{}/'.format(sys.argv[1])        
        min_id = int(sys.argv[2]) if argnum >= 3 else config.min_id
        max_id = int(sys.argv[3]) if argnum >= 4 else config.max_id
        
        scrape_run(url, min_id, max_id)
    except KeyboardInterrupt:
        print('\nExiting...')
        exit(0)


