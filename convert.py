#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
from pprint import pprint
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
		text = fp.read()
		text = text.replace('[]', '')
		print text
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
		print "index: ", i
		print result
		latitude, longitude = geocode(result[u'address'])
		result["lat"] = latitude
		result["lng"] = longitude
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


