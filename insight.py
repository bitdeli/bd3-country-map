from bitdeli.insight import insight
from bitdeli.widgets import Text, Map

@insight
def view(model, params):    
    yield Text(size=(12, 'auto'),
               label='Showing all users',
               data={'text': "## What is the geographic distribution of users?\n"})

    yield Map(id='map',
              size=(12, 6),
              data={ccode: len(uids)
                    for (ccode, uids) in dict(model).iteritems()})
