# tgscraper
Quick and dirty public Telegram group message scraper

# Usage
```bash
$ python3 tgscrape.py <groupname> [minid] [maxid]
```

Example 1:
```bash
$ python3 tgscrape.py fun_with_friends 1 1000
```
dumps messages with ID 1 through 1000 from the group @fun_with_friends

Example 2:
```bash
$ python3 tgscrape.py fun_with_friends
```
dumps messages starting from ID 1 (default value) and stops when it finds 20 (default value) consecutive empty messages.

Retrieved messages are stored in json format in the `conversations` folder.

# Requirements
BeautifulSoup4, requests
```bash
$ pip install -r requirements.txt
```
