from collections import Counter
from bitdeli import textutil
from bitdeli.insight import insight
from bitdeli.widgets import Text, Bar, Map

TOP_COUNT = 10

def country_label(ccode):
    name = textutil.country_name(ccode)
    return "%s (%s)" % (name, ccode) if name else ccode

@insight
def view(model, params):
    yield Text(size=(12, 'auto'),
               label='Showing all users',
               data={'text': "## What is the geographic distribution of users?\n"})

    countries = Counter({ccode: len(uids)
                         for ccode, uids in model.items()})

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
              segmentable=False,
              data=[(country_label(ccode), count)
                    for ccode, count in countries.most_common(TOP_COUNT)])
    
