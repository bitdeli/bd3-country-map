from bitdeli.model import model

def latest_country(events):
    for tstamp, group, ip, event in events:
        if 'geo_country_code' in event:
            return event['geo_country_code']
        elif 'facebook_country' in event:
            return event['facebook_country']

@model
def build(profiles):
    for profile in profiles:
        if 'events' in profile:
            ccode = latest_country(profile['events'])
            if ccode:
                yield ccode, profile.uid
