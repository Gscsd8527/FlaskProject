from .code import *


MsgFlags = {
    SUCCESS:        'ok',
    ERROR:          'fail',
    INVALID_PARAMS: "请求参数错误"
}


def GetMsg(code):
    """
    返回信息
    :param code:
    :return:
    """
    msg = MsgFlags.get(code)
    if msg:
        return msg
    else:
        return MsgFlags[ERROR]
