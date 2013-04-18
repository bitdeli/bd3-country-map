import re
from collections import Counter

from bitdeli import textutil
from bitdeli.insight import insight, segment, segment_label
from bitdeli.widgets import Widget, Text, Bar, Map

class TokenInput(Widget):
    pass

TOP_COUNT = 10

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

def country_users(model, chosen=[]):
    for ccode, uids in model.items():
        if len(chosen) == 0 or ccode in chosen:
            if len(uids) > 0:
                yield ccode, len(uids)

@insight
def view(model, params):
    chosen = []
    if 'countries' in params:
        chosen = list(unique([parse_label(label) for label in params['countries']['value']]))
    
    yield Text(size=(12, 'auto'),
               label='Showing all users',
               data={'text': "## What is the geographic distribution of users?\n"})
    
    yield TokenInput(id='countries',
                     size=(12, 1),
                     label='Filter countries',
                     value=[country_label(ccode) for ccode in chosen],
                     data=[country_label(ccode) for ccode in model.keys()])
    
    countries = Counter(dict(country_users(model, chosen)))

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
