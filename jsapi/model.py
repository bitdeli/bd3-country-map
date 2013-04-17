from bitdeli.model import model

@model
def build(profiles):
    for profile in profiles:
        events = frozenset(event['$event_name']
                           for tstamp, group, ip, event in profile['events'])
        uid = profile.uid
        for event in events:
            yield event, uid
