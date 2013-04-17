from bitdeli.model import model
import GeoIP

geoip = GeoIP.open('/usr/share/geoip/GeoLiteCity.dat', GeoIP.GEOIP_STANDARD)

def latest_country(events):
    for tstamp, group, ip, event in events:
        if 'geo_country_code' in event:
            print 'geo_country_code: %s' % event['geo_country_code']
            return event['geo_country_code']
        elif 'facebook_country' in event:
            print 'facebook_country: %s' % event['facebook_country']
            return event['facebook_country']
        elif 'ip' in event:
            print 'ip: %s' % geoip.record_by_addr(event['ip'])
            return geoip.record_by_addr(event['ip'])
        else:
            return geoip.record_by_addr(ip)

@model
def build(profiles):
    for profile in profiles:
        if 'events' in profile:
            ccode = latest_country(profile['events'])
            if ccode:
                yield ccode, profile.uid
