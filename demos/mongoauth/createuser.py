#!/usr/bin/env python
# coding: utf-8

import hashlib
import txmongo
from twisted.internet import defer, reactor

@defer.inlineCallbacks
def main():
    mongo = yield txmongo.MongoConnection()

    admin = yield mongo.mydb.users.find_one({"u":"cyclone"})
    if admin:
        print "user 'cyclone' with password 'cyclone' already exists: %s" % admin["_id"]
    else:
        objid = yield mongo.mydb.users.insert({"u":"cyclone", "p":hashlib.md5("cyclone").hexdigest()}, safe=True)
        print "user 'cyclone' with password 'cyclone' has been created: %s" % objid

if __name__ == "__main__":
    main().addCallback(lambda ign: reactor.stop())
    reactor.run()
