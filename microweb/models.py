# -*- coding: utf-8 -*-
#:Progetto:  microweb -- models
#:Creato:    Wed 26 Feb 2014 07:49:09 PM CET
#:Autore:    xavi <xavi@asus>
#:Licenza:   GNU General Public License version 3 or later
#

from microweb import db

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)

    def __repr__(self):
        return '<User %r>' % (self.nickname)


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
