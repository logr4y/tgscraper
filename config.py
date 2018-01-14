#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

# script parameters
max_err = 20
min_id = 1                          # first message
max_id = -1                         # no limit
sleeptime = 0.5                     # half second sleep
output_folder = './conversations/'  # output folder

# classes for messages
text_class = 'tgme_widget_message_text'
photo_class = 'tgme_widget_message_photo_wrap'
video_class = 'tgme_widget_message_video_wrap'
voice_class = 'tgme_widget_message_voice'
link_class = 'tgme_widget_message_link_preview'
link_title_class = 'link_preview_site_name'
link_description_class = 'link_preview_description'
link_preview_class = 'link_preview_right_image'
author_class = 'tgme_widget_message_author_name'
service_class = 'message_media_not_supported_label'
meta_class = 'tgme_widget_message_meta'

# message object
message_object = """
{
    "datetime": "",
    "name": "",
    "username": "",
    "quote": "",
    "deleted": "0",
    "msg": "",
    "photo": "",
    "video": "",
    "voice": "",
    "link": {
        "title": "",
        "description": "",
        "preview": ""
    }
}
"""
message_object = json.loads(message_object)