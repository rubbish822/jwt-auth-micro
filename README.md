# jwt-auth-micro
Django microservice JWT authentication use Django-rest-framework

```
from rest_framework.viewsets import ModelViewSet
from jwt_auth.decorators import jwt_login


class SectionViewSet(ModelViewSet):
    queryset = SomeModel.objects.filter(is_active=True)
    serializer_class = SomeModelSerializer
    
    @jwt_login
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
        
```
