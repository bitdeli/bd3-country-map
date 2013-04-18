from collections import namedtuple
from bitdeli.model import model, segment_model

def newest(attr, top=1):
    items = ((iter(hours).next()[0], value)
             for value, hours in attr.iteritems())
    if top == 1:
        return max(items)[1]
    else:
        return [(value, datetime.utcfromtimestamp(hour * 3600).isoformat())
                for hour, value in sorted(items)][-top:]  

@model
def build(profiles):
    for profile in profiles:
        props = profile["properties"]
        if "mp_country_code" in props:
            yield newest(props["mp_country_code"]), profile.uid

@segment_model
def segment(model, segments, labels):
    return namedtuple('SegmentInfo', ('model', 'segments', 'labels'))\
                     (model, segments, labels)
