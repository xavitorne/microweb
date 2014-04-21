"""
Imagine that you have your application in your development machine, and also have
a copy deployed to a production server that is online and in use.

Let's say that for the next release of your app you have to introduce a change
to your models, for example a new table needs to be added. Without migrations
you would need to figure out how to change the format of your database,
both in your development machine and then again in your server,
and this could be a lot of work.

With this database migration support, then when you are ready to release the new
version of the app to your production server you just need to record a new
migration, copy the migration scripts to your production server and run a
simple script that applies the changes for you.
"""

from migrate.versioning import api
from microweb import db
from config import SQLALCHEMY_DATABASE_URI as uri
from config import SQLALCHEMY_MIGRATE_REPO as repo
import imp

import logging

logger = logging.getLogger(__name__)
if logger.isEnabledFor(logging.DEBUG):
    debug = logger.debug
else:
    def debug(message, *args):
        pass

def show_version():
    version = str(api.db_version(uri, repo))
    print 'Current database version: ' + version


def create():
    """Create database and db_repository directory
    for SQLAlchemy-migrate files"""

    import os.path
    from migrate.exceptions import DatabaseAlreadyControlledError
    # create db and models
    db.create_all()

    # create version on database repository migrate
    if not os.path.exists(repo):
        api.create(repo, 'database repository')
        api.version_control(uri, repo)
    else:
        version = api.version(repo)
        try:
            api.version_control(uri, repo, version)
        except DatabaseAlreadyControlledError:
            pass

def migrate():
    """Compare the database against the app models and make a migration
    and upgrade to that version"""

    version = api.db_version(uri, repo) + 1
    migration = repo + '/versions/%03d_migration.py' % version
    tmp_module = imp.new_module('old_model')
    old_model = api.create_model(uri, repo)
    exec old_model in tmp_module.__dict__
    script = api.make_update_script_for_model(uri,
                                              repo,
                                              tmp_module.meta, db.metadata)
    open(migration, "wt").write(script)
    api.upgrade(uri, repo)

    print 'New migration saved as ' + migration
    show_version()


def upgrade():
    """Database will be updated to the lastest version by applying
    the migration scripts in the database repository"""

    api.upgrade(uri, repo)
    show_version()


def downgrade():
    """Database will be downgrade to the previous version"""

    v = api.db_version(uri, repo)
    api.downgrade(uri, repo, v - 1)
    show_version()



def main():
    import argparse

    parser = argparse.ArgumentParser(description="Microweb DB setup.",
                                     epilog="Create the database, or"
                                     " upgrade it to latest patchlevel.")

    parser.add_argument('--version', dest='version',
                        default=True, action='store_true',
                        help='Show db version')
    parser.add_argument('--create', dest='create_db',
                        default=False, action='store_true',
                        help='Create db')
    parser.add_argument('--migrate', dest='migrate_db',
                        default=False, action='store_true',
                        help='Migrate db')
    parser.add_argument('--upgrade', dest='upgrade_db',
                        default=False, action='store_true',
                        help='Upgrade db')
    parser.add_argument('--downgrade', dest='downgrade_db',
                        default=False, action='store_true',
                        help='Downgrade db')

    args = parser.parse_args()

    if args.create_db:
        debug('Creating db...')
        create()

    elif args.migrate_db:
        debug('Migrate db...')
        migrate()

    elif args.upgrade_db:
        debug('Upgrade db...')
        upgrade()

    elif args.downgrade_db:
        debug('Downgrade db...')
        downgrade()
    else:
        if args.version:
            debug('Show version db...')
            show_version()

if __name__ == '__main__':
    main()
