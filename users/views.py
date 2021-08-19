import json, re, bcrypt, requests, jwt

from django.views         import View
from django.http          import JsonResponse

from users.models         import User

from my_settings          import SECRET_KEY, const_algorithm, temporary_password, temporary_phone_number, rest_apt_key

class SignUpView(View):
    def post(self, request):
        try:
            data            = json.loads(request.body)
            email           = data['email']
            password        = data['password']
            hashed_password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())

            if User.objects.filter(email=email).exists():
                return JsonResponse({"MESSAGE": "EMAIL_ALREADY_EXIST"}, status=400)

            if not re.match(r"^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
                return JsonResponse({"MESSAGE": "INVALID_FORMAT"}, status=400)

            if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$", password):
                return JsonResponse({"MESSAGE": "INVALID_FORMAT"}, status=400)

            User.objects.create(
                email        =   email,
                password     =   hashed_password.decode('UTF-8'),
                phone_number =   data['phone_number'],
                nickname     =   data.get('nickname'),
                address      =   data.get('address'),
                user_image   =   data.get('user_image'),
                birthday     =   data.get('birthday'),
            )
            return JsonResponse({"MESSAGE": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)      
            email    = data['email']
            password = data['password']        

            if not User.objects.filter(email = email).exists():
                return JsonResponse({'MESSAGE':'INVALID_VALUE'}, status = 401)

            user = User.objects.get(email=email)
            if bcrypt.checkpw(password.encode('utf-8'),user.password.encode('utf-8')):
                token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm=const_algorithm)
            
                return JsonResponse({'TOKEN': token }, status = 200)

            return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)

class KakaoSignInCallBackView(View):
    def get(self, request):
        try:
            access_token = request.headers.get("Authorization")

            if not access_token :
                return JsonResponse({"MESSAGE": "INVALID_TOKEN"}, status = 401)

            profile_request = requests.get(
                "https://kapi.kakao.com/v2/user/me", headers={"Authorization" : f"Bearer {access_token}"},
            )
            profile_json = profile_request.json()

            kakao_account = profile_json.get("kakao_account")
            email         = kakao_account.get("email")
            kakao_id      = profile_json.get("id")

            hashed_password = bcrypt.hashpw(temporary_password.encode('UTF-8'), bcrypt.gensalt())

            user, created = User.objects.get_or_create(
                kakao_number=kakao_id,
                defaults = {'email' : email,
                'password' : hashed_password.decode('UTF-8'),
                'phone_number' : temporary_phone_number,}
                )

            token = jwt.encode({"id" : user.id}, SECRET_KEY, algorithm=const_algorithm)

            return JsonResponse({"Token" : token}, status = 200)

        except KeyError:
            return JsonResponse({"message" : "INVALID_TOKEN"}, status = 400)