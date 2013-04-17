from bitdeli.insight import insight
from bitdeli.widgets import Text

@insight
def view(model, params):
    yield Text(size=(12, 'auto'),
               label='Showing all users',
               data={'text': "## What is the geographic distribution of users?\n"})
