# -*- coding: utf-8 -*-
#:Progetto:  microweb -- downgrade db
#:Creato:    Wed 26 Feb 2014 08:14:02 PM CET
#:Autore:    xavi <xavi@asus>
#:Licenza:   GNU General Public License version 3 or later
#

#!flask/bin/python
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, v - 1)
print 'Current database version: ' + str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO))
