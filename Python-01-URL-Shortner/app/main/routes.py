from flask import render_template, flash, redirect, url_for, request, abort, jsonify
from app.main import bp
from app.models import URL
from app import db
from app.main.forms import URLForm
from datetime import datetime

@bp.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()
    if form.validate_on_submit():
        url = URL(original_url=form.url.data)
        db.session.add(url)
        db.session.commit()
        flash('URL successfully shortened!')
        return redirect(url_for('main.short_url', short_code=url.short_code))
    return render_template('index.html', form=form)

@bp.route('/<short_code>')
def redirect_to_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first_or_404()
    url.increment_clicks()
    return redirect(url.original_url, code=302)

@bp.route('/url/<short_code>')
def short_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first_or_404()
    short_url = url_for('main.redirect_to_url', short_code=url.short_code, _external=True)
    return render_template('short_url.html', url=url, short_url=short_url)

@bp.route('/stats/<short_code>')
def url_stats(short_code):
    url = URL.query.filter_by(short_code=short_code).first_or_404()
    return render_template('short_url.html', url=url)

@bp.route('/api/shorten', methods=['POST'])
def api_shorten_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'Missing URL parameter'}), 400
    
    form = URLForm(data={'url': data['url']})
    if form.validate():
        url = URL(original_url=form.url.data)
        db.session.add(url)
        db.session.commit()
        short_url = url_for('main.redirect_to_url', short_code=url.short_code, _external=True)
        return jsonify({'short_url': short_url, 'original_url': url.original_url}), 201
    else:
        return jsonify({'error': 'Invalid URL'}), 400

@bp.route('/api/stats/<short_code>')
def api_url_stats(short_code):
    url = URL.query.filter_by(short_code=short_code).first_or_404()
    return jsonify({
        'short_code': url.short_code,
        'original_url': url.original_url,
        'clicks': url.clicks,
        'created_at': url.created_at.isoformat()
    })