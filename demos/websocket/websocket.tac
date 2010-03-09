#!/usr/bin/env python
# test: twistd -ny websocket.tac
# point your browser to http://localhost:8888


import cyclone.web
from twisted.application import service, internet


class MainHandler(cyclone.web.RequestHandler):
    def get(self):
        self.render("interact.html")


class WebSocketHandler(cyclone.web.WebSocketHandler):
    def connectionMade(self, *args, **kwargs):
        print "connection made:", args, kwargs

    def messageReceived(self, message):
        self.sendMessage("echo: %s" % message)
#        self.transport.loseConnection()

    def connectionLost(self, why):
        print "connection lost:", why


class WebSocketApplication(cyclone.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/websocket", WebSocketHandler),
        ]

        settings = { "template_path": "." }
        cyclone.web.Application.__init__(self, handlers, **settings)


application = service.Application("websocket")
internet.TCPServer(8888, WebSocketApplication(),
    interface="127.0.0.1").setServiceParent(application)
