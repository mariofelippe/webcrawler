from flask import Blueprint, render_template, request
from app.classes.crawler import Crawler

bp = Blueprint('site',__name__)

cr = Crawler()

@bp.route('/')
def index():
    
    if request.method == 'GET':
         
        q = request.args.get('q')
        param = request.args.get('param')
        if q:            
           
            cr.get_page(q)
            info = cr.get_info()
            urls = cr.get_urls(text=True, limpa_parametros=param)
            metas = cr.get_meta()
            
            return render_template('busca.html', q=q, info=info, urls=urls, metas=metas)
        
    return render_template('index.html')


