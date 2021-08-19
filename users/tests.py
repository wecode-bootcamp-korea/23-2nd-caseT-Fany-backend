import json, bcrypt, unittest, requests

from django.db import models

from django.http import response
from django.test import TestCase, Client

from unittest.mock import Mock, MagicMock, call, patch

from users.models import User
from users.views import SignUpView, KakaoSignInCallBackView
from my_settings import temporary_password

class UserTest(TestCase):
    def setup(self):
        self.signup = SignUpView()

    def tearDown(self):
        User.objects.all().delete()

    def test_usersignupview_post_success(self):
        client = Client()
        user = {
            'email' : 'seunghun12@wecode.com',
            'password' : 'wecode12#',
            'phone_number' : '010-1111-1111',
        }
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),
        {
            'MESSAGE':'SUCCESS'
        })

    def test_usersignupview_post_keyerror(self):
        client = Client()
        user = {
            'email' : 'jeongillee201@gmail.com',
        }
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                "MESSAGE": "KEY_ERROR"
            }
        )

class KakaoTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        User.objects.all().delete()

    @patch('users.views.requests')    
    def test_kakaologin_view_get_signup_success(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    'id': '1408384944',
                    'kakao_account': {
                    'email' : 'seunghun12@wecode.com'
                    }}
    
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {'HTTP_Authorization' : 'fake_access_token'}
        response            = client.get('/users/kakaocallback', ContentType ='application/json', **headers)

        self.assertEqual(response.status_code, 200)

        @patch('users.views.requests')
        def test_kakao_get_no_token(self, request):
            client   = Client()
            
            response = client.get('/users/kakaocallback')
            self.assertEqual(response.json(),{'MESSAGE':'INVALID_TOKEN'})
            self.assertEqual(response.status_code, 401) 

        @patch('users.views.requests')
        def test_kakao_get_no_data(self, request):
            client = Client()

            class MockedResponse:
                def json(self):
                    return {}

            request.get = MagicMock(return_value = MockedResponse())
            header      = {'HTTP_Authorization' : 'access_token'}
            response    = client.get('/users/kakaocallback', ContentType ='application/json',**header)
            self.assertEqual(response.json(), {'message':'invalid_token'})
            self.assertEqual(response.status_code, 400)