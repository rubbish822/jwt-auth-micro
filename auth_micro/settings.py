# coding: utf-8
from django.conf import settings


JWT_TOKEN_KEY = getattr(settings, 'JWT_TOKEN_KEY', 'jwt')
JWT_EXPIRE_TIME = getattr(settings, 'JWT_EXPIRE_TIME', 3600)
JWT_AUTH_SECRET_KEY = getattr(settings, 'JWT_AUTH_SECRET_KEY', 'JWT_AUTH_SECRET_KEY')
JWT_USER_PK = getattr(settings, 'JWT_USER_PK', 'id')
JWT_REDIS_KEY = getattr(settings, 'JWT_REDIS_KEY', 'user:jwt:{user_id}')

