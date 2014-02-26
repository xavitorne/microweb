# -*- coding: utf-8 -*-
#:Progetto:  microweb -- flask
#:Creato:    Tue 25 Feb 2014 18:39:18 AM CET
#:Autore:    xavi <xavi@airpim.com>
#:Licenza:   GNU General Public License version 3 or later
#

from flask import request, session, redirect, url_for, abort, \
     render_template, flash

from microweb import app, db
from models import Page, Post
from forms import LoginForm


@app.route('/blog/<int:entry_id>')
def show_page(entry_id):
    page = Page.query.get(entry_id)
    return render_template('show_page.html', page=page)


@app.route('/blog')
def show_pages():
    pages = Page.query.all()
    return render_template('show_pages.html', pages=pages)


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/<page_name>')
def specific_page(page_name):
    return render_template('%s' % page_name)


@app.route('/add', methods=['POST'])
def add_page():
    if not session.get('logged_in'):
        abort(401)
    page = Page(title=request.form['title'],
         text=request.form['text'],
         user_id=1)
    db.session.add(page)
    db.session.commit()
    flash('New page was successfully posted')
    return redirect(url_for('show_pages'))


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
            return redirect(url_for('show_pages'))
    return render_template('login.html', error=error, form=form)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_pages'))
