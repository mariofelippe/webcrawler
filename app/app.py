from flask import Flask
from app.blueprints import site, api

def create_app():
    app = Flask(__name__)
    site.init_app(app)
    api.init_app(app)
    
    
    app.run(debug=True)
    
    