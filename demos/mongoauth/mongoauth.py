#!/usr/bin/env python
# coding: utf-8

import sys
import hashlib
import cyclone.web
from twisted.python import log
from twisted.internet import threads, reactor
from pymongo.connection import Connection

class BaseHandler(cyclone.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        self.write('great! <a href="/auth/logout">logout</a>')

class LoginHandler(BaseHandler):
    def get(self):
        err = self.get_argument("e", None)
        self.write("""
            <html><body><form action="/auth/login" method="post">
            username: <input type="text" name="u"><br>
            password: <input type="password" name="p"><br>
            <input type="submit" value="sign in"><br>
            %s
            </body></html>
        """ % (err == "invalid" and "invalid username or password" or ""))

    @cyclone.web.asynchronous
    def post(self):
        u, p = self.get_argument("u"), self.get_argument("p")

        # defer the authentication to a thread, to avoid blocking
        # because pymongo is not asynchronous
        d = threads.deferToThread(self._auth_user, u, p)
        d.addCallback(self._on_auth)

    def _auth_user(self, u, p):
        try:
            users = self.settings.mongo.users # users collection
            if users.find_one({"u":u, "p":hashlib.md5(p).hexdigest()}):
                return u
        except: pass

    def _on_auth(self, user):
        # user is either the username or None
        if user:
            self.set_secure_cookie("user", user)
            self.redirect("/")
        else:
            self.redirect("/auth/login?e=invalid")

class LogoutHandler(BaseHandler):
    @cyclone.web.authenticated
    def get(self):
        self.clear_cookie("user")
        self.redirect("/")

class Application(cyclone.web.Application):
    def __init__(self):
        mongo = Connection() # mongodb connection
        handlers = [
            (r"/", MainHandler),
            (r"/auth/login", LoginHandler),
            (r"/auth/logout", LogoutHandler),
        ]
        settings = dict(
            login_url="/auth/login",
            cookie_secret="32oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            mongo=mongo.cyclone, # cyclone database
        )
        cyclone.web.Application.__init__(self, handlers, **settings)

def main(port):
    reactor.listenTCP(port, Application())
    reactor.run()

if __name__ == '__main__':
    log.startLogging(sys.stdout)
    main(8888)
