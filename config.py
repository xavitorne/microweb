# -*- coding: utf-8 -*-
#:Progetto:  microweb -- config
#:Creato:    Tue 25 Feb 2014 12:21:01 PM CET
#:Autore:    xavi <xavi@airpim.com>
#:Licenza:   GNU General Public License version 3 or later
#

import os

from microweb import app

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'microweb.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

DEBUG=True
DATABASE=os.path.join(basedir, 'microweb.db')
USERNAME='admin'
PASSWORD='admin'
SECRET_KEY='$cippalippa!'
CSRF_ENABLED=True
