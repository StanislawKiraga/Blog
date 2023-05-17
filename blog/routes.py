from flask import Flask, request, redirect, render_template, url_for, flash, session
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm, LoginForm
import functools

@app.route("/")
def index():
    all_posts = Entry.query.filter_by(
        is_published=True).order_by(Entry.pub_date.desc())

    return render_template("homepage.html", all_posts=all_posts)


def login_required(view_func):
   @functools.wraps(view_func)
   def check_permissions(*args, **kwargs):
       if session.get('logged_in'):
           return view_func(*args, **kwargs)
       return redirect(url_for('login', next=request.path))
   return check_permissions


@app.route("/new-post/", methods=["GET", "POST"])
@app.route('/edit-post/<int:entry_id>', methods=['GET', 'POST'])
@login_required
def create_or_edit_entry(entry_id=None):
    if entry_id:
        entry = Entry.query.filter_by(id=entry_id).first_or_404()
        form = EntryForm(obj=entry)
    else:
        form = EntryForm()

    errors = None
    if request.method == 'POST':
        if form.validate_on_submit():
            if entry_id:
                form.populate_obj(entry)
            else:
                entry = Entry(
                    title=form.title.data,
                    body=form.body.data,
                    is_published=form.is_published.data
                )
                db.session.add(entry)
            flash('Wpis został dodany!')
            db.session.commit()
            return redirect(url_for('index'))
        else:
            errors = form.errors
    if not entry_id:
        return render_template("entry_form.html", form=form, errors=errors)
    else:
        return render_template('edit_entry.html', form=form, errors=errors)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    errors = None
    next_url = request.args.get('next')
    if request.method == 'POST':
        if form.validate_on_submit():
            session['logged_in'] = True
            session.permanent = True
            flash('You are now logged in.', 'success')
            return redirect(next_url or url_for('index'))
        else:
            errors = form.errors
    return render_template('login_form.html', form=form, errors=errors)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        flash('You are logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/drafts', methods=['GET'])
@login_required
def list_drafts():
    drafts = Entry.query.filter_by(is_published=False).order_by(Entry.pub_date.desc())

    return render_template("drafts.html", drafts=drafts)

@app.route('/delete_entry/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    if request.method == 'POST':
        db.session.delete(entry)
        db.session.commit()
        flash('Wpis został usunięty!')
        return redirect(url_for('index'))
    return render_template('drafts.html')