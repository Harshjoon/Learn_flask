from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db   import get_db

bp = Blueprint('report', __name__)

@bp.route('/')
def index():
    db = get_db()
    reports = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM reports p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('report/index.html', reports=reports)

@bp.route('/create', methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        body  = request.form["body"]
        error = None

        if not title:
            error = "Title is required"

        if error is not None:
            flash(error)

        else:
            db = get_db()
            db.execute(
                "INSERT INTO reports (title, body, author_id)"
                " VALUES (?,?,?)",
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('report.index'))
    return render_template('report/create.html')


def get_report(id, check_author=True):
    report = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM reports p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()
    
    if report is None:
        abort(404, f"Report id {id} doesn't exist.")

    if check_author and report['author_id'] != g.user['id']:
        abort(403)
    
    return report

@bp.route('/<int:id>/update', methods=("GET", "POST"))
@login_required
def update(id):
    report = get_report(id)

    if request.method == "POST":
        title = request.form['title']
        body  = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE reports SET title = ?, body = ?'
                ' WHERE is = ?'
            )
            db.commit()
            return redirect(url_for('report.index'))
    return render_template('report/update.html', report=report)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_report(id)
    db = get_db()
    db.execute(
        'DELETE FROM reports WHERE id = ?', (id,)
    )
    db.commit()
    return redirect(url_for('report.index'))



