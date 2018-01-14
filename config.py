#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

# message object
message_object = dict()
message_object['datetime'] = str()
message_object['name'] = str()
message_object['username'] = str()
message_object['quote'] = str()
message_object['msg'] = str()
message_object['photo'] = str()
message_object['video'] = str()
message_object['voice'] = str()
message_object['link'] = dict()
message_object['link']['title'] = str()
message_object['link']['description'] = str()
message_object['link']['preview'] = str()
message_object['msg'] = '0'
