# jwt-auth-micro
Django microservice JWT authentication use Django-rest-framework


### default settings
```
JWT_TOKEN_KEY = 'jwt' #jwt eyJhbGciOiJIUzUxMiJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJpdmFuIn0.yYJg8ULMhCpOj5u0d7m4QuJ6FvfKa3lAuA1trZjnSmwZKaZ-TeviN81NmY9E33CdLdJXpWAitBe1ZQTa4xbFwQ
JWT_EXPIRE_TIME = 3600 # token expire time
JWT_AUTH_SECRET_KEY = 'JWT_AUTH_SECRET_KEY'
JWT_USER_PK = 'id'
```

###1. use decorator
```
from rest_framework.viewsets import ModelViewSet
from jwt_auth.decorators import jwt_login


class SectionViewSet(ModelViewSet):
    queryset = SomeModel.objects.filter(is_active=True)
    serializer_class = SomeModelSerializer
    
    @jwt_login  # will use django caches
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
        
```
###2.
```
from auth_micro.auth import set_jwt_token_redis, get_user_data


user_data = {'id': 1, 'username': 'ivan'}
set_jwt_token_redis('user:1:token', user_data) # will use django caches

```

### Or
```
from auth_micro.auth import jwt_token, get_user_data, set_redis_cache, check_jwt_token


user_data = {'id': 1, 'username': 'ivan'}
redis_key = 'user:1:jwt'
token_key = jwt_token(user_data)
# token_key b'eyJhbGciOiJIUzUxMiJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJpdmFuIn0.yYJg8ULMhCpOj5u0d7m4QuJ6FvfKa3lAuA1trZjnSmwZKaZ-TeviN81NmY9E33CdLdJXpWAitBe1ZQTa4xbFwQ'

# store token_key to redis(1 hour)
set_redis_cache(redis_key, token_key.decode(), 60*60)

user_data = get_user_data(token_key)
#user_data {'id': 1, 'username': 'ivan'}

# check_jwt_token(will use django cache)
result = check_jwt_token(redis_key, token_key.decode())
if result:
    # your code
    pass

```
### 3. logout/注销
```
from auth_micro.auth import jwt_logout


jwt_logout(token_key)
```