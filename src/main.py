import re
import json
import argparse
import os
from datetime import datetime
from typing import Final, Dict

import requests
from bs4 import BeautifulSoup

HEADERS: Final[Dict[str, str]] = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-GB,en;q=0.9,nl;q=0.8",
    "cache-control": "max-age=0",
    "dnt": "1",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36 Edg/92.0.902.67",
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Where to write the results to",
        default=os.path.join("", "output.json")
    )
    args = parser.parse_args()

    url = "https://www.justetf.com/en/etf-list-overview.html"
    response = requests.get(url, headers=HEADERS, timeout=30)

    if response.status_code != 200:
        print("Failed to access site '%s' with error: %s" % (url, response.status_code))

    soup = BeautifulSoup(response.text, "lxml")

    # justETF's Overview uses scripts to load the data into the tables
    # at the time of writing this, all the scripts' id attributes start with 'id'
    # for some reason reading the <tr> tags directly doesn't return any values
    data_script_tags = soup.find_all(name="script", id=re.compile("id"))

    # transforming the following structure:
    # /*<![CDATA[*/
    # var id545Etfs = [{...}, {...}];
    # /*]]>*/
    # into [[{}, {}]] for further parsing
    raw_data_list = []
    for tag in data_script_tags:
        content = tag.string.replace("/*<![CDATA[*/", "").replace("/*]]>*/", "").strip()
        opening_bracket_pos = content.find("[")
        closing_bracket_pos = content.find("]") + 1
        raw_data_list.append(json.loads(content[opening_bracket_pos:closing_bracket_pos]))

    # List of list of dictionaries to single dictionary with ticker as key
    etfs = {}
    for inner_list in raw_data_list:
        for item in inner_list:
            etfs[item['wkn']] = item
    
    print("Writing results to %s" % args.output)
    with open(args.output, "w") as f:
        json.dump(etfs, f, ensure_ascii=False)
    