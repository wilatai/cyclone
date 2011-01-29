#!/usr/bin/env python
# coding: utf-8
#
# Copyright 2010 Alexandre Fiori
# based on the original Tornado by Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import sys
import cyclone.web
from twisted.python import log
from twisted.internet import reactor

class MainHandler(cyclone.web.RequestHandler):
    no_keep_alive = False
    def get(self):
        self.write("Hello, world")

class OtherHandler(cyclone.web.RequestDispatcherHandler):
    """
    Example of using the RequestDispatcherHandler instead
    of the RequestHandler.
    """
    no_keep_alive = False

    def index(self):
        self.write('Index')

    def page1(self):
        self.write("Page 1")

    def page2(self):
        self.write("Page 2")

def main():
    application = cyclone.web.Application([
        (r"/", MainHandler),
        (r"/test/.*", OtherHandler),
    ], xheaders=True)

    reactor.listenTCP(8888, application)
    reactor.run()

if __name__ == "__main__":
    log.startLogging(sys.stdout)
    main()
