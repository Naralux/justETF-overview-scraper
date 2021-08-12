# justETF-overview-scraper
Simple scraper which can be used to scrape justETF's complete ETF overview (https://www.justetf.com/en/etf-list-overview.html).
Build for personal use. I have no intention of actively maintaining this.
# Installation
I'd recommened using a virtual environment and activating it before installing dependencies (see Python's [Virtual Environments and Packages docs](https://docs.python.org/3/tutorial/venv.html "Python3 venv docs")):
```
python -m venv venv
```
Install the required packages:
```
pip install -r requirements.txt
```
# Usage
Simply run `main.py` from the command line:
```
python .\src\main.py
```
# Notes
This is my first web scraper, first time using Python and the first time using Beautifulsoup4. Therefor the code won't be as clean or efficient as it could/should be. I'm always open to feedback, tips & tricks!
