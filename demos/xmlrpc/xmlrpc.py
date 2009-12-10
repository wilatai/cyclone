#!/usr/bin/env python
# coding: utf-8

import sys
import cyclone.web
import cyclone.httpclient
from twisted.python import log
from twisted.internet import defer, reactor

class MainHandler(cyclone.web.RequestHandler):
    def get(self):
        self.write("hello world!")

class XmlrpcHandler(cyclone.web.XmlrpcRequestHandler):
    allowNone = True

    def xmlrpc_echo(self, text):
        return text

    def xmlrpc_sort(self, items):
        return sorted(items)

    @defer.inlineCallbacks
    @cyclone.web.asynchronous
    def xmlrpc_geoip_lookup(self, address):
        result = yield cyclone.httpclient.fetch("http://freegeoip.net/xml/%s" % address)
        defer.returnValue(result.body)

def main():
    application = cyclone.web.Application([
        (r"/", MainHandler),
        (r"/xmlrpc", XmlrpcHandler),
    ])

    reactor.listenTCP(8888, application)
    reactor.run()

if __name__ == "__main__":
    log.startLogging(sys.stdout)
    main()
