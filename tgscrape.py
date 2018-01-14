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
import copy
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


def parse_message(soup):
    """ Parses a message, returns object """
    datetime = soup.find('time')['datetime']
    return_object = copy.deepcopy(config.message_object)
    if datetime:
        (name, username) = get_sender(soup)
        return_object['datetime'] = datetime
        return_object['name'] = name
        return_object['username'] = username

        msg = soup.find_all('', class_=config.text_class)
        if msg:
            if len(msg) == 2:
                quote = msg[0].text
                msg = msg[1].text
            else:
                msg = msg[0].text
                quote = None
            
            return_object['msg'] = msg
            if quote:
                return_object['quote'] = quote
        
        service_msg = soup.find('', class_=config.service_class)
        if service_msg:
            return_object['msg'] = '[SERVICE MESSAGE]'

        media = soup.find('', class_=config.photo_class) or \
            soup.find('', class_=config.video_class) or \
            soup.find('', class_=config.voice_class) or \
            soup.find('', class_=config.link_class)

        if media:
            if media['class'][0] == config.photo_class:
                return_object['photo'] = media['style'].split("'")[1]

            if media['class'][0] == config.video_class:
                return_object['video'] = media.video['src']

            if media['class'][0] == config.voice_class:
                return_object['voice'] = media.audio['src']

            if media['class'][0] == config.link_class:
                title_class = soup.find('', class_=config.link_title_class)
                description_class = soup.find('', class_=config.link_description_class)
                preview_class = soup.find('', class_=config.link_preview_class)
                return_object['link'] = {}
                return_object['link']['title'] = title_class.text if title_class else ''
                return_object['link']['description'] = description_class.text \
                                                        if description_class else ''
                return_object['link']['preview'] = preview_class['style'].split("'")[1] \
                                                        if preview_class else ''

        return return_object


def print_object(lobj):
    """ Print a message object """
    if 'deleted' in lobj.keys():
        print('[deleted]')
        return

    outputline = '[{}] {}{}: '.format(lobj['datetime'],
                                      lobj['name'],
                                      ' (@{})'.format(lobj['username']) if lobj['username'] else '')
    outputline += '{}{}'.format('{{ {} }} '.format(lobj['quote']) if lobj['quote'] else '',
                                lobj['msg'])
    outputline += ' {}'.format(lobj['photo']) if lobj['photo'] else ''
    outputline += ' {}'.format(lobj['video']) if lobj['video'] else ''
    outputline += ' {}'.format(lobj['voice']) if lobj['voice'] else ''
    outputline += ' <{}>'.format(" - ".join([lobj['link']['title'],
                                             lobj['link']['description'],
                                             lobj['link']['preview']
                                            ])) if lobj['link']['title'] or \
                                                   lobj['link']['description'] or \
                                                   lobj['link']['preview'] \
                                                   else ''
    print(outputline)


def scrape_run(lgroupname, lmi n_id, lmax_id, ldb):
    """ Main logic """
    msg_id = lmin_id
    cnt_err = 0
    url = 'https://t.me/{}/'.format(lgroupname)
    while True:
        db_index = str(msg_id)
        if db_index not in ldb.keys():
            r_url = url + db_index + '?embed=1'
            response = requests.get(r_url)
            if len(response.text) > 3000:
                cnt_err = 0
                soup_object = BeautifulSoup(response.text, 'html.parser')
                ldb[db_index] = parse_message(soup_object)
            else:
                ldb[db_index] = copy.deepcopy(config.message_object)
                ldb[db_index]['deleted'] = '1'
                cnt_err += 1
                if cnt_err == config.max_err:
                    for id_to_delete in range(msg_id, msg_id - config.max_err, -1):
                        del ldb[str(id_to_delete)]
                    return '{} consecutive empty messages. Exiting...'.format(config.max_err)
            time.sleep(config.sleeptime)

        print_object(ldb[db_index])

        if msg_id == lmax_id:
            return 'All messages retrieved. Exiting...'

        msg_id += 1


try:
    print('> Telegram Public Groups Scraper\n')
    argnum = len(sys.argv)

    if argnum < 2:
        print(usage(sys.argv[0]))
        raise ValueError('\nNot enough parameters')

    groupname = sys.argv[1]
    min_id = int(sys.argv[2]) if argnum >= 3 else config.min_id
    max_id = int(sys.argv[3]) if argnum >= 4 else config.max_id
    
    dh = db.DB(groupname)
    database = dh.load_data()
    exit_msg = scrape_run(groupname, min_id, max_id, database)
    exit_code = 0
except KeyboardInterrupt:
    exit_code = 1
    exit_msg = 'Exiting...'
except ValueError as e:
    exit_code = 1
    exit_msg = e
finally:
    print('\r  ')
    try:
        dh.write_data(database)
    except NameError:
        pass
    print(exit_msg)
    exit(exit_code)
