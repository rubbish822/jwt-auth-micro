# coding: utf-8
import typing

from django.core.cache import cache, caches
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer, JSONWebSignatureSerializer
from itsdangerous.exc import BadSignature, BadTimeSignature

from .exceptions import (JwtDecodeError, JwtExpireError, JwtNotRightError)


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
    expire_time = expire_time or getattr(settings, 'JWT_EXPIRE_TIME', 3600)
    serializer = TimedJSONWebSignatureSerializer(secret_key, expires_in=expire_time)
    return serializer.dumps(user_data)


def set_redis_cache(
        key: str,
        data: typing.Any,
        expire_time: int=None,
        cache_name: str='default'
) -> typing.Any:
    """
    将jwt数据储存到redis中
    :param key:
    :param data:
    :param expire_time:
    :param cache_name: cache 名称
    :return:
    """
    assert key, 'The key is required!'
    caches[cache_name].set(key, data, timeout=expire_time)


def get_redis_cache(
        key: str,
        cache_name: str='default',
) -> typing.Any:
    """
    获取redis数据
    :param key:
    :param cache_name:
    :return:
    """
    return caches[cache_name].get(key)


def get_header_token(request):
    """
    获取header中的jwt token
    :param request:
    :return:
    """
    token_key = request.META.get('HTTP_AUTHORIZATION', '')
    jwt_token_key = getattr(settings, 'JWT_TOKEN_KEY', 'jwt ')
    token = ''
    if token_key is not None:
        token = token_key.replace(jwt_token_key, "")
    return token


def decode_jwt_token(
        key: str,
        request: typing.Any,
        secret_key: str=settings.JWT_AUTH_SECRET_KEY,
        cache_name: str='default',
) -> typing.Any:
    """
    解密token中的用户数据
    :param key: redis的key
    :param request: Request实例
    :param secret_key:
    :param cache_name: cache名称
    :return:
    """
    token_key = get_header_token(request)
    serializer = JSONWebSignatureSerializer(secret_key)
    try:
        user_data = serializer.loads(token_key)
    except (BadSignature, Exception) as e:
        raise JwtNotRightError
    check_jwt_token(key, token_key, cache_name)
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
        key: str,
        request: typing.Any,
        secret_key: str=settings.JWT_AUTH_SECRET_KEY,
        cache_name: str='default',
        expire_time: int=None,
) -> typing.Any:
    """
    解密token中的用户数据
    :param key: redis的key
    :param request: Request实例
    :param secret_key:
    :param cache_name: cache名称
    :param expire_time: 过期时间, 为None时表示永远不过期
    :return:
    """
    token_key = get_header_token(request)
    serializer = TimedJSONWebSignatureSerializer(secret_key, expires_in=expire_time)
    try:
        user_data = serializer.loads(token_key)
    except (BadSignature, Exception) as e:
        raise JwtNotRightError
    check_jwt_token(key, token_key, cache_name)
    request.user = user_data
    return user_data, None
