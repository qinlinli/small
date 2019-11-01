import json

from flask import Response

from miniapp.exc.errmsg import errmsg
from miniapp.exc import codes


def json_res(data, http_code):
    return Response(data, status=http_code, mimetype='application/json')


def success(data, http_code=codes.HTTP_OK, **kwargs):
    resp = {'code': codes.CODE_OK, 'result': data}
    if kwargs:
        resp.update(kwargs)
    data = json.dumps(resp)
    return json_res(data, http_code)


def fail(http_code, code, msg=None, result=None):
    if msg is None:
        msg = errmsg.get(code, '')
    payload = {'code': code, 'error': msg}
    if result is not None:
        payload['result'] = result
    data = json.dumps(payload)
    return json_res(data, http_code)