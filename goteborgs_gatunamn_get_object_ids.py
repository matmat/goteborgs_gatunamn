#!/usr/bin/env python3

import requests
import xml.etree.ElementTree as ET
import re
import sys

carlotta_base_url            = "https://samlingar.goteborgsstadsmuseum.se"
carlotta_advanced_search_path = "/carlotta/web/perform/advanced_search"
carlotta_query_url           = carlotta_base_url + carlotta_advanced_search_path
carlotta_object_browse_path  = "/carlotta/web/perform/object_browse"
carlotta_object_browse_url   = carlotta_base_url + carlotta_object_browse_path


ortnamn_register = "13018268"
spe = "OBJNAMN"
varde_gatunamn_object = "Värde, gatunamn"
operation = "EXISTS"

object_ids = list()


# https://samlingar.goteborgsstadsmuseum.se/carlotta/web/perform/advanced_search?register=13018268&spe_1=OBJNAM&obj_1=V%C3%A4rde%2C+gatunamn&op_1=EXISTS
resp=requests.get(carlotta_query_url, [('register', ortnamn_register), ('spe_1', spe), ('obj_1', varde_gatunamn_object), ('op_1', operation)])
doc_root=ET.fromstring(resp.text)

# Format is e.g "Ortnamn (6,515)"
number_of_hits = doc_root.find(".//*[@class='register_filter']").text
number_of_hits = int(''.join(re.findall(r'[^\D]',number_of_hits)))


#    print(status)
for n in range(number_of_hits):

    resp = requests.get(carlotta_object_browse_url, \
      [('browseEnvironment', \
           carlotta_advanced_search_path + '?' \
           + '&'.join(['register=' + ortnamn_register, \
                       'spe_1='    + spe, \
                       'obj_1='    + varde_gatunamn_object, \
                       'op_1='     + operation])), \
        ('detailBrowseIndex', n)], \
    allow_redirects=False)

    object_id = resp.headers['Location'].split(';')[0].split("/")[-1]

#    object_ids.add(object_id)
    object_ids.append(object_id)

    print(object_id)
    print(n, object_id, file=sys.stderr)

#print("antal: ",len(object_ids))
