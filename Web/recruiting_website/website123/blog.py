from flask import (
    Blueprint, g, render_template, request, url_for
)
from werkzeug.exceptions import abort

from website123.db import get_db

import math

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    db = get_db()
    max_page = math.ceil(
        db.execute('select number from jobs'
        ' order by number desc limit 1'
        ).fetchone()['number'] / 30
    )
    pages = list(range(1, max_page + 1))
    jobs = db.execute(
        'select number, title'
        ' from jobs order by number desc'
        ' limit 30'
    ).fetchall()
    return render_template('blog/index.html', jobs=jobs, pages=pages)


def get_infos(number):
    infos = get_db().execute(
        'select title, state, detail, post_date'
        ' from jobs where number=?', (number,)
        ).fetchone()
    return infos

@bp.route('/<int:number>', methods=['GET'])
def detail(number):
    infos = get_infos(number)
    return render_template('blog/detail.html', infos=infos)


@bp.route('/job-board?page=<int:number>')
def job_board(number):
    db = get_db()
    max_page = math.ceil(
        db.execute('select number from jobs'
        ' order by number desc limit 1'
        ).fetchone()['number'] / 30
    )
    pages = list(range(1, max_page + 1))
    jobs = db.execute(
        'select number, title'
        ' from jobs order by number desc'
        ' limit 30 offset ?', ((number - 1) * 30, )
    ).fetchall()
    return render_template('blog/index.html', jobs=jobs, pages=pages)