# -*- coding: utf-8 -*-
#:Progetto:  microweb -- db migration and update structure
#:Creato:    Wed 26 Feb 2014 08:01:29 PM CET
#:Autore:    xavi <xavi@asus>
#:Licenza:   GNU General Public License version 3 or later
#

#!flask/bin/python
import imp
from migrate.versioning import api
from microweb import db
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO

migration = SQLALCHEMY_MIGRATE_REPO + '/versions/%03d_migration.py' % (api.db_version(SQLALCHEMY_DATABASE_URI,
                                                SQLALCHEMY_MIGRATE_REPO) + 1)
tmp_module = imp.new_module('old_model')
old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
exec old_model in tmp_module.__dict__
script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI,
                                          SQLALCHEMY_MIGRATE_REPO,
                                          tmp_module.meta, db.metadata)
open(migration, "wt").write(script)
api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print 'New migration saved as ' + migration
print 'Current database version: ' + str(api.db_version(SQLALCHEMY_DATABASE_URI,
                                                        SQLALCHEMY_MIGRATE_REPO))
