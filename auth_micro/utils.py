# coding: utf-8
import typing

from django.core.cache import caches
from django.conf import settings
from .exceptions import (TokenHeaderError, )
from . import settings as jwt_settings


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


def remove_jwt_token(
        key: str,
        cache_name: str='default'
) -> typing.NoReturn:
    """
    删除redis中的jwt数据
    :param key:
    :param cache_name:
    :return:
    """
    assert key, 'The key is required!'
    caches[cache_name].delete(key)


def get_header_token(request):
    """
    获取header中的jwt token
    :param request:
    :return:
    """
    token_key = request.META.get('HTTP_AUTHORIZATION', '')
    jwt_token_key = getattr(settings, 'JWT_TOKEN_KEY', jwt_settings.JWT_TOKEN_KEY)
    if token_key is not None:
        return token_key.replace(jwt_token_key, '').replace(' ', '')
    raise TokenHeaderError
