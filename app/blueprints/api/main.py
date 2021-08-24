from flask import Blueprint, jsonify, request
from app.classes.crawler import Crawler


bp = Blueprint('api', __name__, url_prefix="/api/")

cr = Crawler()

@bp.route('/')
def index():
    response = {'Consulta informação da url': '/info/(url)','Retornar as URLs da página': '/links/(url)', 'Retornar as URLs detalhadas':'/links/(url)/text'}
    status = 200
    return jsonify(response), status

@bp.route('/info/')
@bp.route('/info/<url>')
def info(url=None):
    
    
    if url:
        if cr.get_page(url):
            info = cr.get_info()
            response = {'url_request': url, 'info': info}
            status = 200
        else:
            response = 'A URL {} informada é inválida!'.format(q)
            status = 400
    else:
        response = {'Consulta informação da url':'/info/(url)'}
        status = 200
        
    return jsonify(response), status

@bp.route('/links/')
@bp.route('/links/<url>')
@bp.route('/links/<url>/<text>')
def links(url=None, text=False):
    print(url, text)
    
    if text:
        text = text.lower()
    if text == 'true' or text == 'text':
        text = True
    else:
        text = False
    if url:
        if cr.get_page(url):
            info = cr.get_info()
            links = cr.get_urls(text=text)
            response = {'url_request':url, 'info': info, 'links': links}
            status = 200
        else:
            response = 'A URL {} informada é inválida!'.format(url)
            status = 400
    else:
        response = {'Retornar as URLs da página': '/links/(url)', 'Retornar as URLs detalhadas':'/links/(url)/text'}
        status = 200
    return jsonify(response), status



@bp.route('/images/<url>')
def images(url):
    
    response = {'ola':'mundo'}
    status = 200
    return jsonify(response), status