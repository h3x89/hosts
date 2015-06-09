#!/usr/bin/python

import sys
import socket

for arg in sys.argv[1:]:
	hostname = arg
	ip = socket.gethostbyname(hostname)
	hostname_full = socket.gethostbyaddr(ip)[0]
	print("""
### %s ###
_client_NAME = "%s"
_client_IP = "%s"
_client_PORT = 6556
_client_TAGS = "|LINUX"     
_client_GROUPS = ""

_client_NAME_PORT_TAGS =  str(str(_client_NAME) + "|" + str(_client_PORT) + str(_client_TAGS) + str(_client_GROUPS))

all_hosts  += [ _client_NAME_PORT_TAGS ]
ipaddresses.update({ _client_NAME : _client_IP })
agent_ports += [( _client_PORT, [ str(_client_PORT) ], all_hosts )]
""" % ( hostname, hostname_full, ip ))
