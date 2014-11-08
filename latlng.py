#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
# from xml.etree.ElementTree import fromstring
import xml.dom.minidom
ENCODING = 'utf-8'

def geocode(address):
    url = u"http://maps.google.com/maps/api/geocode/xml?&language=ja&sensor=false&region=ja&address="
    url = url + urllib.quote(address.encode(ENCODING))
    buffer = urllib.urlopen(url).read()
    # xml = fromstring(buffer)
    # lat = float(xml.find('GeocodeResponse/result/geometry/location/lat').text)
    # lng = float(xml.find('GeocodeResponse/result/geometry/location/lng').text)
    dom = xml.dom.minidom.parseString(buffer)
    lat = float(dom.getElementsByTagName("lat")[0].childNodes[0].data)
    lng = float(dom.getElementsByTagName("lng")[0].childNodes[0].data)
    return lat, lng

if __name__ == '__main__':
	print geocode(u'大岡山')