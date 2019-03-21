# coding: utf-8
from rest_framework.request import Request

from .auth import decode_jwt_token


def jwt_login(func):
    def wrapper(*args, **kwargs):
        request = None
        for count, thing in enumerate(args):
            if type(thing) is Request:
                request = args[count]
                break
        decode_jwt_token(request)
        return func(*args, **kwargs)
    return wrapper
