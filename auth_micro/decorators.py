# coding: utf-8
from rest_framework.request import Request
from rest_framework.exceptions import AuthenticationFailed

from .auth import decode_jwt_token, decode_jwt_token_expire
from .exceptions import JwtNotRightError, JwtExpireError


def jwt_login(func):
    def wrapper(*args, **kwargs):
        request = None
        for count, thing in enumerate(args):
            if type(thing) is Request:
                request = args[count]
                break
        try:
            decode_jwt_token(request)
        except (JwtNotRightError, JwtExpireError, Exception):
            raise AuthenticationFailed
        return func(*args, **kwargs)
    return wrapper


def jwt_login_expire(func):
    def wrapper(*args, **kwargs):
        request = None
        for count, thing in enumerate(args):
            if type(thing) is Request:
                request = args[count]
                break
        try:
            decode_jwt_token_expire(request)
        except (JwtNotRightError, JwtExpireError, Exception):
            raise AuthenticationFailed
        return func(*args, **kwargs)
    return wrapper
