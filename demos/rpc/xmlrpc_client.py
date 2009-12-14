#!/usr/bin/env python
# coding: utf-8

import xmlrpclib

srv = xmlrpclib.Server("http://localhost:8888/xmlrpc")
print "echo:", srv.echo("hello world!")
print "sort:", srv.sort(["foo", "bar"])
print "count:", srv.count(["foo", "bar"])
print "geoip_lookup:\n", srv.geoip_lookup("google.com")
