#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import urllib2
import xml.dom.minidom
import time
from pprint import pprint
import matplotlib
from plot3d import create_3d_bar
from latlng import geocode
import logging
import traceback

dummy = '''[
	{
		"address": "石川台",
		"name": "自宅",
		"value": 10.0
	},
	{
		"address": "東京工業大学",
		"name": "大学",
		"value": 20.0
	},
	{
		"address": "大岡山駅",
		"name": "最寄り駅",
		"value": 30.0
	}
]'''

if len(sys.argv) >= 2:
	with open(sys.argv[1], 'r') as fp:
		# lines = []
		# for line in fp.readlines():
		# 	if line.find("/*") >= 0:
		# 		continue
		# 	if line.find("_id") >= 0:
		# 		continue
		# 	lines.append(line)

		# text = ''.join(lines)
		text = fp.read()
		# text = text.replace('}', '},')
		text = text.replace('[]', '')
		# index = text.rfind(',')
		# textlist = list(text)
		# textlist[index] = " "
		# text = "".join(textlist)
		print text
		# with open("json.txt", "w") as fp:
		# 	fp.write(text)
		info = json.loads(text)
elif len(sys.argv) == 1:
	info = json.loads(dummy)

if not os.path.exists("images"):
	os.makedirs("images")

delete_list = []
info = info['rows']
out = []
for i, item in enumerate(info):
	try:
		result = item[u'value']
		# time.sleep(3.0)
		print "index: ", i
		print result
		# query = "http://www.geocoding.jp/api/?q=" + item['address'].encode('utf-8', 'ignore')
		# response = urllib2.urlopen(query)
		# xml_contents = response.read()
		# dom = xml.dom.minidom.parseString(xml_contents)
		# latitude = float(dom.getElementsByTagName("lat")[0].childNodes[0].data)
		# longitude = float(dom.getElementsByTagName("lng")[0].childNodes[0].data)
		# print "lat: ", latitude
		# print "lng: ", longitude
		latitude, longitude = geocode(result[u'address'])
		result["lat"] = latitude
		result["lng"] = longitude
		# path = os.path.join("images", "%s.png" % time.strftime("%d_%H%M%S"))
		# create_3d_bar(path, float(item['price'].replace(',', '')))
		# item['bar'] = path
		print latitude
		print longitude
		result['value'] = float(result[u'price'].replace(',', ''))
		out.append(result)
	except:
		delete_list.append(item)
		logging.error(traceback.format_exc())
		continue

for item in delete_list:
	info.remove(item)

pprint(out)
with open("data.json", "w") as fp:
	fp.write(json.dumps(out))


