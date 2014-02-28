# -*- coding: utf-8 -*-
#:Progetto:  microweb -- models
#:Creato:    Wed 26 Feb 2014 07:49:09 PM CET
#:Autore:    xavi <xavi@asus>
#:Licenza:   GNU General Public License version 3 or later
#
from werkzeug.security import generate_password_hash, \
     check_password_hash

from microweb import db

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    password = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)


class Page(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), index = True, unique = True)
    text = db.Column(db.String(1000))
    lang = db.Column(db.String(4))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return '<Page %r>' % (self.title)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
