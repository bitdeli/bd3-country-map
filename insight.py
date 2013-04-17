import re
from collections import Counter

from bitdeli import textutil
from bitdeli.insight import insight, segment, segment_label
from bitdeli.widgets import Text, Bar, Map

TOP_COUNT = 10

def country_label(ccode):
    name = textutil.country_name(ccode)
    return "%s (%s)" % (name, ccode) if name else ccode

def country_users(model):
    for ccode, uids in model.items():
        if len(uids) > 0:
            yield ccode, len(uids)

@insight
def view(model, params):
    print list(model.keys())
    
    yield Text(size=(12, 'auto'),
               label='Showing all users',
               data={'text': "## What is the geographic distribution of users?\n"})
    
    countries = Counter({ccode: count
                         for ccode, count in country_users(model)})

    label = '{0[0]:,} users in {0[1]:,} countries'
    totals = (sum(countries.values()),
              len(countries))
    
    yield Map(id='map',
              size=(12, 6),
              data=countries,
              label=label.format(totals))
    
    yield Bar(id='top_countries',
              label='Top %d countries' % TOP_COUNT,
              size=(12, 4),
              data=[(country_label(ccode), count)
                    for ccode, count in countries.most_common(TOP_COUNT)])

def segment_country(params):
    label = params['value']['label']
    if len(label) == 2:
        return label
    return re.search('\((\w\w)\)$', label).group(1)
    
@segment
def segment(model, params):
    return model[segment_country(params)]
    
@segment_label
def label(segment, model, params):
    ccode = segment_country(params)
    return 'Users from %s' % textutil.country_name(ccode)
