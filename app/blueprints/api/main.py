from flask import Blueprint, render_template, request
from app.classes.crawler import Crawler

bp = Blueprint('api', __name__, url_prefix="/api/")

cr = Crawler()

@bp.route('/')
def index():
    return '{"api": "minha api"}'


@bp.route('/info/')
def info():
    q = request.args.get('q')
    
    cr.get_page(q)
    info = cr.get_info()
    data = {'url_request':q, 'data': info}
   
    return data


@bp.route('/links/')
def links():
    q = request.args.get('q')
   
    return '{}'.format(q)