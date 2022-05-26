#!/usr/bin/env python3

import requests
import xml.etree.ElementTree as ET
import re
from bs4 import BeautifulSoup
import json
import pprint
import urllib.parse
import fileinput
import sys
from itertools import islice

def get_dl(soup):
    keys, values = [], []

    for tag in soup.find_all("span",class_="hidden"):
        tag.decompose()

    for tag in soup.find_all("dl", class_="object_sub_description"):
        tag.decompose()

    for dl in soup.findAll("dl"):
        for dt in dl.findAll("dt"):
            keys.append(dt.get_text("\n").strip())
        for dd in dl.findAll("dd"):
            values.append(dd.get_text("\n\n").strip())
    return dict(zip(keys, values))




carlotta_base_url            = "https://samlingar.goteborgsstadsmuseum.se"
carlotta_object_path         = "/carlotta/web/object"
carlotta_object_url          = carlotta_base_url + carlotta_object_path

#objects = [1375460,2111523,1377563,1381895,1379146]

lines = fileinput.input()
objects = [_.strip() for _ in lines]

#objects = [1375462,1375464,1375460,2111523,1377563,1381895,1379146,1376428,1377736,1378372,1379085,1380440,1381952,1762486]
#objects = [1376428,1377736,1377826,1378372,1378372,1379085,1380440,1381952,1762486]

gatunamn = {}


for object in objects:
    object_url = carlotta_object_url + "/" + str(object)

    gatunamn[object_url] = {}

    resp = requests.get(object_url)

    print("object:", object, file=sys.stderr)


    soup = BeautifulSoup(resp.text, 'html.parser')

    for tag in soup.find_all("span",class_="hidden"):
        tag.decompose()

    for tag in soup.find_all("dl", class_="object_sub_description"):
        tag.decompose()
    
    for tag in soup.find_all("dt", class_="object_description"):
        tag.parent.decompose()

    for dl in soup.findAll("dl"):
        for dt in islice(dl.children, 0, None, 2):
            dd = dt.next_sibling
            for tag in dd.find_all(["a", "img", "span"]):
                tag.unwrap()
            attr_value = " ".join(map(str, dd.contents)).strip()


            if dt.get_text() != "\n":
                attr_key = dt.string.strip()
                gatunamn[object_url][attr_key] = attr_value
            else:
                for prev_dt in islice(dt.previous_siblings, 1, None, 2):
                    if prev_dt.get_text() != "\n":
                        attr_key = prev_dt.string.strip()
                        break

                gatunamn[object_url][attr_key] += "; " + attr_value


#    keys, values = [], []
#    for dl in soup.findAll("dl"):
#        for dt in dl.findAll("dt"):
#            if dt.get_text() == "\n":
#                attr_desc = "FIXME: Empty key"
#            else:
#                attr_desc = dt.string.strip()
#            obj_id = dt.a['href'].split(';')[0].split('/')[-1]
#            keys.append(attr_desc)
#        for dd in dl.find_all("dd"):
#            for tag in dd.find_all(["a", "img", "span"]):
#                tag.unwrap()
#
#            desc_string = " ".join(map(str, dd.contents)).strip()
#
#            values.append(desc_string)

#    gatunamn[carlotta_object_url + "/" + str(object)] = dict(zip(keys, values))

print(json.dumps(gatunamn, sort_keys=True, indent=4, ensure_ascii=False))

#    dl_dict = get_dl(soup)

#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(gatunamn)

#    print(json.dumps(dl_dict, sort_keys=True, indent=4, ensure_ascii=False))

#    print(dl_dict.keys())



#for status in status_gatunamn:
#    resp=requests.get(carlotta_query_url, [('dataelement', status_gatunamn_dataelement), ('value_urlencoded',status), ('op', operation)])
#    doc_root=ET.fromstring(resp.text)
#
#    # Format is e.g "Ortnamn (6,515)"
#    number_of_hits = doc_root.find(".//*[@class='register_filter']").text
#    number_of_hits = int(''.join(re.findall(r'[^\D]',number_of_hits)))
#
#
#    print(status)
#    for n in range(number_of_hits):
#
#        resp=requests.get(carlotta_object_browse_url, [('browseEnvironment', carlotta_element_search_path + '?' + '&'.join(['dataelement=' + status_gatunamn_dataelement, 'op=' + operation, 'value=' + status])), ('detailBrowseIndex', n)],allow_redirects=False)
#
#        object_id = resp.headers['Location'].split(';')[0].split("/")[-1]
#
#        object_ids.add(object_id)
#        object_ids.append(object_id)
#
#        print(object_id)
#
#    print("antal: ",len(object_ids))
