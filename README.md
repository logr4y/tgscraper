# tgscraper
Quick and dirty public Telegram group message scraper

# Usage
```bash
$ python3 tgscrape.py <groupname> [minid] [maxid]
```

Example:
```bash
$ python3 tgscrape.py fun_with_friends 1 1000
```
dumps messages with ID 1 through 1000 from the group @fun_with_friends

The loop stops when it finds 20 consecutive empty messages

# Requirements
BeautifulSoup4, requests
```bash
$ pip install -r requirements.txt
```
