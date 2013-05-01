from itertools import chain
from collections import namedtuple
from bitdeli.model import model, segment_model
from bitdeli.segment_discodb import make_segment_view
import GeoIP

geoip = GeoIP.open('/usr/share/geoip/GeoLiteCity.dat', GeoIP.GEOIP_STANDARD)

def latest_country(events):
    for tstamp, group, ip, event in events:
        # Adding support for custom country code properties:
        # if 'country_code' in event:
        #     return event['country_code']
        record = geoip.record_by_addr(event.get('ip', ip))
        if record:
            return record['country_code']

@model
def build(profiles):
    for profile in profiles:
        source_events = chain(profile.get('events', []),
                              profile.get('$pageview', []),
                              profile.get('$dom_event', []))
        ccode = latest_country(source_events)
        if ccode:
            yield ccode, profile.uid

@segment_model
def segment(model, segments, labels):
    return namedtuple('SegmentInfo', ('model', 'segments', 'labels', 'view'))\
                     (model, segments, labels, make_segment_view(model, segments))
