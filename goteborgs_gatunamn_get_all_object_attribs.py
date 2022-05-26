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

#objects = [1375462,1375464,1376428]

attribs = {}


for object in objects:
    resp = requests.get(carlotta_object_url + "/" + str(object))

    print("object:", object, file=sys.stderr)


    soup = BeautifulSoup(resp.text, 'html.parser')

    keys, values = [], []
    
    for tag in soup.find_all("span",class_="hidden"):
        tag.decompose()

    for tag in soup.find_all("dl", class_="object_sub_description"):
        tag.decompose()
    
    for tag in soup.find_all("dt", class_="object_description"):
        tag.parent.decompose()

    for dl in soup.findAll("dl"):
        for dt in dl.findAll("dt"):
#            print(dt)
            if dt.get_text() == "\n":
                continue

#            print(dt)
            obj_id = dt.a['href'].split(';')[0].split('/')[-1]
            obj_desc = dt.a.get_text()
#            print(obj_id, obj_desc)

            if obj_id in attribs:
               attribs[obj_id]['count'] += 1
            else:
                attribs[obj_id] = {}
                attribs[obj_id]['description'] = obj_desc
                attribs[obj_id]['count'] = 1

#            print(attribs[obj_id])

print(json.dumps(attribs, sort_keys=True, indent=4, ensure_ascii=False))



#        for dt in dl.findAll("dt"):
#            keys.append(dt.get_text("\n").strip())
#        for dd in dl.findAll("dd"):
#            values.append(dd.get_text("\n\n").strip())
#    return dict(zip(keys, values))


#    dl_dict = get_dl(soup)

#    pp = pprint.PrettyPrinter(indent=4)
#    pp.pprint(dl_dict)

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
