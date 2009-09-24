#!/usr/bin/env python
# coding: utf-8

import hashlib
from pymongo.connection import Connection

conn = Connection() # localhost
mydb = conn.cyclone # cyclone database
users = mydb.users  # users collection

admin = users.find_one({"u": "cyclone"})
if not admin:
    print "creating user 'cyclone' with password 'cyclone'..."
    users.insert({"u":"cyclone", "p":hashlib.md5("cyclone").hexdigest()})
else:
    print "user 'cyclone' with password 'cyclone' already exists..."
