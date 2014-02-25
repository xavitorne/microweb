# -*- coding: utf-8 -*-
#:Progetto:  microweb -- flask
#:Creato:    Tue 25 Feb 2014 18:39:18 AM CET
#:Autore:    xavi <xavi@airpim.com>
#:Licenza:   GNU General Public License version 3 or later
#
import sqlite3
from flask import request, session, g, redirect, url_for, abort, \
     render_template, flash

from microweb import app
from forms import LoginForm

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


@app.route('/blog/<int:entry_id>')
def show_entry(entry_id):
    db = get_db()
    cur = db.execute('select title, text from entries where entry_id = %s' % entry_id)
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)


@app.route('/blog')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/<page_name>')
def specific_page(page_name):
    return render_template('%s' % page_name)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error, form=form)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
