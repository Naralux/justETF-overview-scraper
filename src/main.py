import re
import json
import argparse
import os
from datetime import datetime
from typing import Final, Dict
from bs4.element import ResultSet

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

def map_ticker_to_data_obj(data_objects):
    temp_mapping = {}
    for obj in data_objects:
        obj_content = obj.string.replace("/*<![CDATA[*/", "").replace("/*]]>*/", "").strip()
        obj_id = obj_content[4:13].strip()

        opening_bracket_pos = obj_content.find("[")
        closing_bracket_pos = obj_content.find("]") + 1
        obj_list = json.loads(obj_content[opening_bracket_pos:closing_bracket_pos])

        temp_mapping[obj_id] = obj_list

    result = {}
    for x in temp_mapping:
        for y in temp_mapping[x]:
            if y['wkn'] is not None:
                result[y['wkn']] = x

    return result

def find_category_by_data_obj(soup: BeautifulSoup):
    equity_category_elements = soup.find_all(name="a", href=re.compile("#equity_"), attrs={"class", "d-inline-block link nolink"})
    # bond_category_elements = soup.find_all(name="a", href=re.compile("#bonds_"), attrs={"class", "d-inline-block link nolink"})

    for tag in equity_category_elements:
        print(tag.find_parent(name="div", id=re.compile("id23")))
    

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
    find_category_by_data_obj(soup)

    # justETF's Overview uses scripts to load the data into the tables
    # at the time of writing this, all the scripts' id attributes start with 'id'
    # for some reason reading the <tr> tags directly doesn't return any values
    data_script_tags = soup.find_all(name="script", id=re.compile("id"))
    map_ticker_to_data_obj(data_script_tags)

    # transforming the following structure:
    # /*<![CDATA[*/
    # var id545Etfs = [{...}, {...}];
    # /*]]>*/
    # into [[{}, {}]] for further parsing
    # raw_data_list = []
    # for tag in data_script_tags:
    #     content = tag.string.replace("/*<![CDATA[*/", "").replace("/*]]>*/", "").strip()
    #     opening_bracket_pos = content.find("[")
    #     closing_bracket_pos = content.find("]") + 1
    #     raw_data_list.append(json.loads(content[opening_bracket_pos:closing_bracket_pos]))

    # # List of list of dictionaries to dict of dicts with ticker as key
    # etfs = {}
    # for inner_list in raw_data_list:
    #     for item in inner_list:
    #         etfs[item['wkn']] = item
    
    # print("Writing results to %s" % args.output)
    # with open(args.output, "w") as f:
    #     json.dump(etfs, f, ensure_ascii=False)
    