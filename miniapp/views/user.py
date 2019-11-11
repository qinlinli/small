from flask import Blueprint, request
from requests import codes

from miniapp.utils.api import success, fail
from models.user import User

bp = Blueprint('miniapp.views', __name__, url_prefix='/api/app/user')


@bp.route('', methods=['POST'])
async def verify_mobile():
    data = request.get_json()
    mobile = data.get('mobile')
    user = User.get_by_mobile(mobile)
    if user:
        return fail(codes.HTTP_OK,
                    codes.CODE_INVALID_REQUEST_DATA,
                    "员工不是审核通过的状态""号码已经注册")
    User.create(data)
    return success("注册成功")
