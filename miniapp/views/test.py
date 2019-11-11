from flask import Blueprint

bp = Blueprint('miniapp', __name__, url_prefix='')


@bp.route('/test')
def test():
    return '测试通过啦,真棒!'