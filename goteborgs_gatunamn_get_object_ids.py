#!/usr/bin/env python3

import requests
import xml.etree.ElementTree as ET
import re


carlotta_base_url            = "https://samlingar.goteborgsstadsmuseum.se"
carlotta_element_search_path = "/carlotta/web/perform/element_search"
carlotta_query_url           = carlotta_base_url + carlotta_element_search_path
carlotta_object_browse_path  = "/carlotta/web/perform/object_browse"
carlotta_object_browse_url   = carlotta_base_url + carlotta_object_browse_path

status_gatunamn_dataelement = "13018275"
status_gatunamn = ["beslutat namn, ej färdig gata",
                   "ej fastställd",
                   "gällande",
                   "införlivad",
                   "tillfälligt namn",
                   "utgått"]

operation = "EQUALS"

object_ids = list()

for status in status_gatunamn:
    resp=requests.get(carlotta_query_url, [('dataelement', status_gatunamn_dataelement), ('value_urlencoded',status), ('op', operation)])
    doc_root=ET.fromstring(resp.text)

    # Format is e.g "Ortnamn (6,515)"
    number_of_hits = doc_root.find(".//*[@class='register_filter']").text
    number_of_hits = int(''.join(re.findall(r'[^\D]',number_of_hits)))


#    print(status)
    for n in range(number_of_hits):

        resp=requests.get(carlotta_object_browse_url, [('browseEnvironment', carlotta_element_search_path + '?' + '&'.join(['dataelement=' + status_gatunamn_dataelement, 'op=' + operation, 'value=' + status])), ('detailBrowseIndex', n)],allow_redirects=False)

        object_id = resp.headers['Location'].split(';')[0].split("/")[-1]

#        object_ids.add(object_id)
        object_ids.append(object_id)

        print(object_id)

#    print("antal: ",len(object_ids))
