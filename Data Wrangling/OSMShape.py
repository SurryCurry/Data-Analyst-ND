# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import re, json, codecs

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
                             
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
street_mapping = {'Ave':'Avenue',
                  'Blvd':'Boulevard',
                  'Dr':'Drive',
                  'Dr.':'Drive',
                  'E':'East',
                  'E.':'East',
                  'N':'North',
                  'N.':'North',
                  'Pkwy':'Parkway',
                  'RD':'Road',
                  'Rd':'Road',
                  'Rd.':'Road',
                  'S':'South',
                  'S.':'South',
                  'SW':'Southwest',
                  'St':'Street',
                  'St.':'Street',
                  'W':'West',
                  'W.':'West'}
city_mapping = {'Columbus, OH':'Columbus',
                'Dublin, OH':'Dublin',
                'POWELL':'Powell',
                'Pickertington':'Pickerington',
                'Reynoldsburh':'Reynoldsburg',
                'columbus':'Columbus',
                'dublin':'Dublin',
                'hilliard':'Hilliard'}
state_mapping = {'OH - Ohio':'OH',
                 'OHIO':'OH',
                 'Oh':'OH',
                 'Ohio':'OH',
                 'oh':'OH'}
country_mapping = {'US':'USA'}
zip_mapping = {'43119-8650-08':'43119',
               '43215-1430':'43215',
               '43220-4800':'43220',
               'OH 43206':'43206'}

def update_name(name, mapping):
    """Helper function for change_names."""
    if name in mapping:
        name=mapping[name]
    return name

def change_names(tag):
    """Function to update undesired names to desired ones,
    using mapping dicts."""
    if 'street' in tag.attrib['k']:
        name=tag.attrib['v'].split()
        for n in name:
            n=update_name(n, street_mapping)
        tag.attrib['v']=' '.join(name)
    elif 'city' in tag.attrib['k']:
        tag.attrib['v']=update_name(tag.attrib['v'], city_mapping)
    elif 'state' in tag.attrib['k']:
        tag.attrib['v']=update_name(tag.attrib['v'], state_mapping)
    elif 'country' in tag.attrib['k']:
        tag.attrib['v']=update_name(tag.attrib['v'], country_mapping)
    elif 'postcode' in tag.attrib['k']:
        tag.attrib['v']=update_name(tag.attrib['v'], zip_mapping)

def shape_element(element):
    """Function to create dicts for each node & way tag in the OSM dataset."""
    node = {}
    if element.tag == "node" or element.tag == "way":
        c={}
        p=[0.0, 0.0]
        ad={}
        for a in element.attrib:
            if a in CREATED:
                c[a]=element.attrib[a]
            elif 'lat' in a:
                p[0]=float(element.attrib[a])
            elif 'lon' in a:
                p[1]=float(element.attrib[a])
            else:
                node[a]=element.attrib[a]
        node['type']=element.tag
        node['created']=c
        node['pos']=p
        for c in element:
            if element.tag=='node':
                k=c.attrib['k']
                if re.search(problemchars, k):
                    pass
                elif re.search(lower_colon, k):
                    kut=k.split(':')
                    if len(kut)>2:
                        pass
                    elif 'addr' in kut:
                        change_names(c)
                        ad[kut[1]]=c.attrib['v']
                        node['address']=ad
                else:
                    node[k]=c.attrib['v']
            elif element.tag=='way':
                r=[]
                if 'k' in c.attrib:
                    k=c.attrib['k']
                    if re.search(problemchars, k):
                        pass
                    elif re.search(lower_colon, k):
                        kut=k.split(':')
                        if len(kut)>2:
                            pass
                        elif 'addr' in kut:
                            change_names(c)
                            ad[kut[1]]=c.attrib['v']
                            node['address']=ad
                    else:
                        node[k]=c.attrib['v']
                elif 'ref' in c.attrib:
                    r.append(c.attrib['ref'])
                    node['node_refs']=r
        return node
    else:
        pass
    
def process_map(file_in, pretty = False):
    """Function to create json file and return list of json objects."""
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, mode="w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data