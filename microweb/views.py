# -*- coding: utf-8 -*-
#:Progetto:  microweb -- flask
#:Creato:    Tue 25 Feb 2014 18:39:18 AM CET
#:Autore:    xavi <xavi@airpim.com>
#:Licenza:   GNU General Public License version 3 or later
#

from flask import request, redirect, url_for, abort, \
     render_template, flash, g
from flask.ext.login import login_user, logout_user, current_user, login_required

from microweb import app, db, lm
from models import Page, User
from forms import LoginForm

@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))



@app.route('/blog/<int:entry_id>')
def show_page(entry_id):
    page = Page.query.get(entry_id)
    return render_template('show_page.html', page=page)


@app.route('/blog')
def show_pages():
    pages = Page.query.all()
    return render_template('show_pages.html', pages=pages)


@app.route('/add_page', methods=['GET', 'POST'])
#@login_required
def add_page():
    if g.user is not None and g.user.is_authenticated():
        if request.method == 'POST':
            page = Page(title=request.form['title'],
                text=request.form['text'],
                user_id=1)
            db.session.add(page)
            db.session.commit()
            flash('New page was successfully posted')
        return render_template('add_pages.html')
        #return redirect(url_for('add_pages'))
    else:
        abort(401)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        flash('You are already logged in')
        return redirect(url_for('show_pages'))
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if user is None:
            error = 'Invalid username'
            return render_template('login.html', error=error, form=form)
        password = request.form['password']
        if not user.check_password(password):
            error = 'Invalid password'
            return render_template('login.html', error=error, form=form)
        else:
            remember_me = form.remember_me.data
            flash('You were logged in')
            login_user(user, remember = remember_me)
            return redirect(url_for('show_pages'))
    return render_template('login.html', error=error, form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You were logged out')
    return redirect(url_for('show_pages'))


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/<page_name>')
def specific_page(page_name):
    return render_template('%s' % page_name)
    #return redirect(url_for('static', filename=page_name))
