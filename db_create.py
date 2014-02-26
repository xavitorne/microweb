# -*- coding: utf-8 -*-
#:Progetto:  microweb -- create db or migrate
#:Creato:    Wed 26 Feb 2014 07:56:53 PM CET
#:Autore:    xavi <xavi@asus>
#:Licenza:   GNU General Public License version 3 or later
#

#!flask/bin/python
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from microweb import db

import os.path
db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))
