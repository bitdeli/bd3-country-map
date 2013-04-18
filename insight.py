import re
from collections import Counter

from bitdeli import textutil
from bitdeli.insight import insight, segment, segment_label
from bitdeli.widgets import Widget, Text, Bar, Map

class TokenInput(Widget):
    pass

TOP_COUNT = 10

CONTINENTS = {
    "Africa":        ["AO","BF","BI","BJ","BW","CD","CF","CG","CI","CM","CV","DJ","DZ","EG","EH","ER","ET","GA","GH","GM","GN","GQ","GW","KE","KM","LR","LS","LY","MA","MG","ML","MR","MU","MW","MZ","NA","NE","NG","RE","RW","SC","SD","SH","SL","SN","SO","ST","SZ","TD","TG","TN","TZ","UG","YT","ZA","ZM","ZW"],
    "Asia":          ["AE","AF","AM","AP","AZ","BD","BH","BN","BT","CC","CN","CX","CY","GE","HK","ID","IL","IN","IO","IQ","IR","JO","JP","KG","KH","KP","KR","KW","KZ","LA","LB","LK","MM","MN","MO","MV","MY","NP","OM","PH","PK","PS","QA","SA","SG","SY","TH","TJ","TL","TM","TW","UZ","VN","YE"],
    "Europe":        ["AD","AL","AT","AX","BA","BE","BG","BY","CH","CZ","DE","DK","EE","ES","EU","FI","FO","FR","FX","GB","GG","GI","GR","HR","HU","IE","IM","IS","IT","JE","LI","LT","LU","LV","MC","MD","ME","MK","MT","NL","NO","PL","PT","RO","RS","RU","SE","SI","SJ","SK","SM","TR","UA","VA"],
    "North America": ["AG","AI","AN","AW","BB","BL","BM","BS","BZ","CA","CR","CU","DM","DO","GD","GL","GP","GT","HN","HT","JM","KN","KY","LC","MF","MQ","MS","MX","NI","PA","PM","PR","SV","TC","TT","US","VC","VG","VI"],
    "Oceania":       ["AS","AU","CK","FJ","FM","GU","KI","MH","MP","NC","NF","NR","NU","NZ","PF","PG","PN","PW","SB","TK","TO","TV","UM","VU","WF","WS"],
    "South America": ["AR","BO","BR","CL","CO","EC","FK","GF","GY","PE","PY","SR","UY","VE"]
}

def unique(events):
    seen = set()
    for event in events:
        if event not in seen:
            yield event
            seen.add(event)

def country_label(ccode):
    name = textutil.country_name(ccode)
    return "%s (%s)" % (name, ccode) if name else ccode

def parse_label(label):
    if len(label) == 2:
        return label
    return re.search('\((\w\w)\)$', label).group(1)

def get_codes(chosen):
    for label in chosen:
        if label in CONTINENTS:
            for ccode in CONTINENTS[label]:
                yield ccode
        else:
            yield parse_label(label)

def country_users(model, codes=[]):
    for ccode, uids in model.items():
        if len(codes) == 0 or ccode in codes:
            if len(uids) > 0:
                yield ccode, len(uids)

@insight
def view(model, params):
    chosen = []
    if 'countries' in params:
        chosen = list(unique(params['countries']['value']))
    
    yield Text(size=(12, 'auto'),
               label='Showing all users',
               data={'text': "## What is the geographic distribution of users?\n"})
    
    choices = [country_label(ccode) for ccode in model.keys()]
    choices.extend(CONTINENTS.keys())
    yield TokenInput(id='countries',
                     size=(12, 1),
                     label='Filter by country or continent',
                     value=chosen,
                     data=choices)
    
    countries = Counter(dict(country_users(model, list(get_codes(chosen)))))

    label = '{users:,} users in {countries:,} countries'
    yield Map(id='map',
              size=(12, 6),
              data=countries,
              label=label.format(users=sum(countries.values()),
                                 countries=len(countries)))
    
    yield Bar(id='top_countries',
              label='Top %d countries' % TOP_COUNT,
              size=(12, 4),
              data=[(country_label(ccode), count)
                    for ccode, count in countries.most_common(TOP_COUNT)])

def segment_country(params):
    widget = params['id']
    if widget == 'map':
        return params['value']
    elif widget == 'top_countries':
        return parse_label(params['value']['label'])
    
@segment
def segment(model, params):
    return model[segment_country(params)]
    
@segment_label
def label(segment, model, params):
    ccode = segment_country(params)
    return 'Users from %s' % textutil.country_name(ccode)
