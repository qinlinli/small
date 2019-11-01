from flask import Flask
from flask import Blueprint

from miniapp.config import load_configs
from miniapp.corelibs.stone import db
from miniapp.views import views_register


def create_app(name=None):
    app = Flask(name or __name__)
    load_configs(app)
    views_register(app)
    db.init_app(app)

    return app


bp = Blueprint('miniapp', __name__, url_prefix='')


@bp.route('/test')
def test():
    return 'ok'
