from bitdeli.model import model
import GeoIP

geoip = GeoIP.open('/usr/share/geoip/GeoLiteCity.dat', GeoIP.GEOIP_STANDARD)

def latest_country(events):
    for tstamp, group, ip, event in events:
        if 'geo_country_code' in event:
            return event['geo_country_code']
        elif 'facebook_country' in event:
            return event['facebook_country']
        elif 'ip' in event:
            return geoip.record_by_addr(event['ip'])
        else:
            return geoip.record_by_addr(ip)

@model
def build(profiles):
    for profile in profiles:
        if 'events' in profile:
            ccode = latest_country(profile['events'])
            print ccode
            if ccode:
                yield ccode, profile.uid
