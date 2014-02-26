# -*- coding: utf-8 -*-
#:Progetto:  microweb -- upgrade db
#:Creato:    Wed 26 Feb 2014 08:14:13 PM CET
#:Autore:    xavi <xavi@asus>
#:Licenza:   GNU General Public License version 3 or later
#

#!flask/bin/python
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print 'Current database version: ' + str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO))
