# coding: utf-8
import typing

from django.conf import settings
from itsdangerous import (TimedJSONWebSignatureSerializer, JSONWebSignatureSerializer)
from itsdangerous.exc import (BadSignature, BadTimeSignature)

from .exceptions import (JwtExpireError, JwtNotRightError, )
from .utils import (get_redis_cache, get_header_token, remove_jwt_token, )
from auth_micro import settings as jwt_settings


def jwt_token(
        user_data: typing.Any,
        secret_key: str=settings.JWT_AUTH_SECRET_KEY,
) -> typing.Any:
    """
     加密用户数据
    :param user_data: 加密的数据
    :param secret_key: 加密的key
    :return:
    """
    serializer = JSONWebSignatureSerializer(secret_key)
    return serializer.dumps(user_data)


def jwt_token_expire(
        user_data: typing.Any,
        secret_key: str=settings.JWT_AUTH_SECRET_KEY,
        expire_time: int=None,
) -> typing.Any:
    """

    :param user_data:
    :param secret_key:
    :param expire_time:
    :return:
    """
    expire_time = expire_time or getattr(
        settings, 'JWT_EXPIRE_TIME', jwt_settings.JWT_EXPIRE_TIME)
    serializer = TimedJSONWebSignatureSerializer(
        secret_key, expires_in=expire_time)
    return serializer.dumps(user_data)


def decode_jwt_token(
        request: typing.Any,
        secret_key: str=settings.JWT_AUTH_SECRET_KEY,
        cache_name: str='default',
        token_key: str='',
) -> typing.Any:
    """
    解密token中的用户数据
    :param request: Request实例
    :param secret_key:
    :param cache_name: cache名称
    :param token_key: jwt token
    :return:
    """
    token_key = token_key or get_header_token(request)
    serializer = JSONWebSignatureSerializer(secret_key)
    try:
        user_data = serializer.loads(token_key)
    except (BadSignature, Exception) as e:
        raise JwtNotRightError
    else:
        user_pk = getattr(settings, 'JWT_USER_PK', jwt_settings.JWT_USER_PK)
        user_id = user_data.get(user_pk, '')
        check_jwt_token(user_id, token_key, cache_name)
    request.user = user_data
    return user_data, None


def check_jwt_token(
        key: str,
        token_key: str,
        cache_name: str='default',
) -> typing.Any:
    """
    检查jwt token是否正确
    :param key: redis 的key
    :param token_key: 解密出来的jwt token
    :param cache_name: 缓存的名字
    :return:
    """
    cache_user_token_key = get_redis_cache(key, cache_name)
    if not cache_user_token_key:
        # token过期
        raise JwtExpireError
    if cache_user_token_key != token_key:
        # 不是最新的/正确的token
        raise JwtNotRightError
    return True


def decode_jwt_token_expire(
        request: typing.Any,
        secret_key: str=settings.JWT_AUTH_SECRET_KEY,
        cache_name: str='default',
        expire_time: int=None,
        token_key: str='',
) -> typing.Any:
    """
    解密token中的用户数据
    :param request: Request实例
    :param secret_key:
    :param cache_name: cache名称
    :param expire_time: 过期时间, 为None时表示永远不过期
    :param token_key: jwt token
    :return:
    """
    token_key = token_key or get_header_token(request)
    serializer = TimedJSONWebSignatureSerializer(secret_key, expires_in=expire_time)
    try:
        user_data = serializer.loads(token_key)
    except (BadSignature, BadTimeSignature, Exception):
        raise JwtNotRightError
    else:
        user_pk = getattr(settings, 'JWT_USER_PK', jwt_settings.JWT_USER_PK)
        user_id = user_data.get(user_pk, '')
        check_jwt_token(user_id, token_key, cache_name)
    request.user = user_data
    return user_data, None


def jwt_logout(
        key: str,
        cache_name: str='default',
) -> typing.NoReturn:
    """
    注销用户token
    :param key:
    :param cache_name:
    :return:
    """
    remove_jwt_token(key, cache_name)
