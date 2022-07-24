from flask import make_response
from .msg import GetMsg
import json


def Response(httpCode, code,  data):
    """
    返回
    :param httpCode:
    :param code:
    :param data:
    :return:
    """
    data_json = {
        'code': code,
        'msg': GetMsg(code),
        'data': data
    }
    print("AAAAAA= ", data_json)
    resp = make_response(json.dumps(data_json, ensure_ascii=False))
    resp.status = httpCode
    return resp
