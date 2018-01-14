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
import db

def usage(pyfile):
    """ Usage """
    return 'Usage: {} <groupname> [minid] [maxid]'.format(pyfile)

def get_sender(obj):
    """ Retrieves the sender of a message """
    author = obj.find('', class_=config.author_class)
    return_name = author.text
    if author.name == 'a':
        return_username = author['href'].split('/')[3]
    elif author.name == 'span':
        return_username = ''

    return (return_name, return_username)

def scrape_run(lgroupname, lmin_id, lmax_id, ldb = {}):
    """ Main logic """
    msg_id = lmin_id
    cnt_err = 0
    url = 'https://t.me/{}/'.format(lgroupname)
    while True:
        r_url = url + str(msg_id) + '?embed=1'
        response = requests.get(r_url)
        ldb[msg_id] = {}
        if len(response.text) > 3000:
            cnt_err = 0
            soup = BeautifulSoup(response.text, 'html.parser')
            datetime = soup.find('time')['datetime']
            if datetime:
                (name, username) = get_sender(soup)
                outputline = '[{}] {}{}: '.format(datetime,
                                        name,
                                        ' (@{})'.format(username) if username else ''
                                        )
                ldb[msg_id]['datetime'] = datetime
                ldb[msg_id]['name'] = name
                ldb[msg_id]['username'] = username

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
                    ldb[msg_id]['msg'] = msg
                    ldb[msg_id]['quote'] = quote
                    

                media = soup.find('', class_=config.photo_class) or \
                    soup.find('', class_=config.video_class) or \
                    soup.find('', class_=config.voice_class) or \
                    soup.find('', class_=config.link_class)

                if media:
                    if media['class'][0] == config.photo_class:
                        outputline += media['style'].split("'")[1]
                        ldb[msg_id]['photo'] = media['style'].split("'")[1]

                    if media['class'][0] == config.video_class:
                        outputline += media.video['src']
                        ldb[msg_id]['video'] = media.video['src']

                    if media['class'][0] == config.voice_class:
                        outputline += media.audio['src']
                        ldb[msg_id]['voice'] = media.video['src']

                    if media['class'][0] == config.link_class:
                        title_class = soup.find('', class_=config.link_title_class)
                        description_class = soup.find('', class_=config.link_description_class)
                        preview_class = soup.find('', class_=config.link_preview_class)
                        outputline += ' [{}{}{}]'.format(
                            title_class.text + ' - ' if title_class else '',
                            description_class.text + ' - ' if description_class else '',
                            preview_class['style'].split("'")[1] if preview_class  else ''
                        )
                        ldb[msg_id]['link'] = {}
                        ldb[msg_id]['link']['title'] = title_class.text if title_class else ''
                        ldb[msg_id]['link']['description'] = description_class.text \
                                                                if description_class else ''
                        ldb[msg_id]['link']['preview'] = preview_class['style'].split("'")[1] \
                                                                if preview_class else ''

                print(outputline)
                outputline = ''

        else:
            print('[deleted]')
            ldb[msg_id]['msg'] = '[deleted]'
            cnt_err += 1
            if cnt_err == config.max_err:
                return '{} consecutive empty messages. Exiting...'.format(config.max_err)

        if msg_id == lmax_id:
            return 'All messages retrieved. Exiting...'

        msg_id += 1
        time.sleep(config.sleeptime)

try:
    print('> Telegram Public Groups Scraper\n')
    argnum = len(sys.argv)

    if argnum < 2:
        print(usage(sys.argv[0]))
        raise Exception('\nNot enough parameters')

    groupname = sys.argv[1]
    min_id = int(sys.argv[2]) if argnum >= 3 else config.min_id
    max_id = int(sys.argv[3]) if argnum >= 4 else config.max_id
    
    dh = db.DB(groupname)
    database = dh.load_data()
    exit_msg = scrape_run(groupname, min_id, max_id, database)
    exit_code = 0
except KeyboardInterrupt:
    exit_code = 1
    exit_msg = '\rExiting...'
except Exception as e:
    exit_code = 1
    exit_msg = e
finally:
    try:
        dh.write_data(database)
    except:
        pass
    print(exit_msg)
    exit(exit_code)


