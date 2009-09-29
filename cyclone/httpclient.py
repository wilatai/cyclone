# coding: utf-8

from twisted.web import client
from cyclone.util import superdict

class Page(superdict):
    pass

class HTTPClientFactory(client.HTTPClientFactory):
    def page(self, page):
        if self.waiting:
            self.waiting = 0
            self.deferred.callback(Page(
                body=page,
                headers=self.response_headers,
                cookies=self.cookies,
            ))

def fetch(url, contextFactory=None, *args, **kwargs):
    return client._makeGetterFactory(url, HTTPClientFactory,
        contextFactory=contextFactory, *args, **kwargs).deferred
