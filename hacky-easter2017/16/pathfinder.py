#!/usr/bin/python3

import urllib.request
import json

def check_path(req):
	resp = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
	print(req.full_url + ' : ' + str(resp))
	if resp['Answer'] == 'This leads to nowhere, so turn around!':
		return False
	elif resp['Answer'] == 'Go on! Follow one of the possible paths' or resp['Answer'] == 'Follow one of the possible paths':
		return resp['paths']
	else:
		print(resp)
		return False

def dfs(req):
	nodes = check_path(req)
	print(nodes)
	if nodes:
		for n in nodes:
			new_req = urllib.request.Request(req.full_url + str(n), None, {'User-Agent': 'PathFinder'})
			dfs(new_req)

req = urllib.request.Request('http://hackyeaster.hacking-lab.com:9999/', None, {'User-Agent': 'PathFinder'})
dfs(req)

