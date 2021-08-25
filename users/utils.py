import jwt

from django.http            import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from users.models           import User
from my_settings            import SECRET_KEY, const_algorithm


def LoginDecorator(func):
    def wrapper(self,request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            payload      = jwt.decode(access_token ,SECRET_KEY, algorithms= const_algorithm)
            user         = User.objects.get(id = payload['id'])
            request.user = user

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message':'INVALID_TOKEN'}, status = 400)
        
        except ObjectDoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=400)

        return func(self,request, *args, **kwargs)
        
    return wrapper