# tgscraper
Quick and dirty public Telegram group message scraper

# Usage
```python3 tgscrape.py <groupname> [minid] [maxid]```

Example:
```python3 tgscrape.py @infosecita 1 1000```
dumps messages 1 through 1000 from the group @infosecita

The loop stops when it finds 20 consecutive empty messages

# Requirements
BeautifulSoup4
requests
```bash
$ pip install -r requirements.txt
```
