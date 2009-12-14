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

    def xmlrpc_count(self, items):
        return len(items)

    @defer.inlineCallbacks
    @cyclone.web.asynchronous
    def xmlrpc_geoip_lookup(self, address):
        result = yield cyclone.httpclient.fetch("http://freegeoip.net/xml/%s" % address)
        defer.returnValue(result.body)

class JsonrpcHandler(cyclone.web.JsonrpcRequestHandler):
    def jsonrpc_echo(self, text):
        return text

    def jsonrpc_sort(self, items):
        return sorted(items)

    def jsonrpc_count(self, items):
        return len(items)

    @defer.inlineCallbacks
    @cyclone.web.asynchronous
    def jsonrpc_geoip_lookup(self, address):
        result = yield cyclone.httpclient.fetch("http://freegeoip.net/xml/%s" % address.encode("utf-8"))
        defer.returnValue(result.body)


def main():
    application = cyclone.web.Application([
        (r"/", MainHandler),
        (r"/xmlrpc", XmlrpcHandler),
        (r"/jsonrpc", JsonrpcHandler),
    ])

    reactor.listenTCP(8888, application)
    reactor.run()

if __name__ == "__main__":
    log.startLogging(sys.stdout)
    main()
