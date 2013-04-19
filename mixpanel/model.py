from collections import namedtuple
from bitdeli.model import model, segment_model
from bitdeli.segment_discodb import make_segment_view

def newest(attr, top=1):
    items = ((iter(hours).next()[0], value)
             for value, hours in attr.iteritems())
    return max(items)[1]

@model
def build(profiles):
    for profile in profiles:
        props = profile["properties"]
        if "mp_country_code" in props:
            yield newest(props["mp_country_code"]), profile.uid

@segment_model
def segment(model, segments, labels):
    return namedtuple('SegmentInfo', ('model', 'segments', 'labels', 'view'))\
                     (model, segments, labels, make_segment_view(model, segments))
