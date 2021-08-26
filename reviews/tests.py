import json, jwt

from django.http import response
from django.test import TestCase, Client

from reviews.models import Review
from products.models import Category, DetailCategory, Product, SubCategory, Size, Color, ProductOption
from users.models import User
from my_settings import SECRET_KEY, const_algorithm

class  ReviewTest(TestCase):
    @classmethod
    def setUpTestData(self):
        User.objects.create(
            email = 'wecode12@wecode.com',
            password = 'wecode12#',
            phone_number = '010-3333-3333'
        )
        user = User.objects.get(email='wecode12@wecode.com')
        self.token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm=const_algorithm)


        Category.objects.create(
            name = 'test'
        )

        SubCategory.objects.create(
            option = 'test2',
            category_id = 1,
        )

        DetailCategory.objects.create(
            detail = 'test3',
            sub_category_id = 1,
        )

        Product.objects.create(
            id = 1,
            name = 'testtest',
            price = 10000,
            detail_category_id = 1,
        )

        Size.objects.create(
            select_size = 'L'
        )

        Color.objects.create(
            name = 'Red',
        )

        ProductOption.objects.create(
            product_id = 1,
            size_id = 1,
            color_id = 1,
            stock = 100,
            sales = 1000,
        )

        Review.objects.create(
            user_id = 1,
            product_id = 1,
            score = 5
        )

    def tearDown(self):
        User.objects.all().delete()
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        DetailCategory.objects.all().delete()
        Product.objects.all().delete()
        Size.objects.all().delete()
        Color.objects.all().delete()
        ProductOption.objects.all().delete()
        Review.objects.all().delete()

    def test_review_create_post_success(self):
        client = Client()
        
        body = {
            'score' : 5
        }

        headers  = {'HTTP_Authorization': self.token}
        response = client.post('/products/1/review', body, **headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
            "MESSAGE": "SUCCESS"
        })

    def test_review_no_score_post_fail(self):
         client = Client()
         body = {
            'score1' : 1
         }

         headers  = {'HTTP_Authorization': self.token}
         response = client.post('/products/1/review', body, **headers)
         self.assertEqual(response.status_code, 404)

    def test_review_get_success(self):
         client = Client() 
         headers  = {'HTTP_Authorization': self.token}
         response = client.get('/products/1/review/1', **headers)
         self.assertEqual(response.status_code, 200)
         self.assertEqual(response.json(),{
             'MESSAGE': {
                'image': None, 
                'product_id': 1,
                'product_name': 'testtest',
                'score': 5,
                'text': None,
                'user': 1}
                }
                )

    def test_review_get_fail(self):
        client = Client()
        headers  = {'HTTP_Authorization': self.token}
        response = client.get('/products/1/review/99999', **headers)
        self.assertEqual(response.status_code, 404)

    def test_review_update_post_success(self):
        client = Client()
        headers  = {'HTTP_Authorization': self.token}
        body = {
            'score' : 1
        }

        response = client.post('/products/1/review', body, **headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
            "MESSAGE": "SUCCESS"
        })

    def test_review_update_post_fail(self):
        client = Client() 
        headers  = {'HTTP_Authorization': self.token}
        body = {
            'score1' : 1,
         }

        response = client.post('/products/1/review', body, **headers)
        self.assertEqual(response.status_code, 404)

    def test_review_delete_success(self):
        client = Client()
        headers  = {'HTTP_Authorization': self.token}
        response = client.delete('/products/1/review/1', **headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "MESSAGE": "SUCCESS"
        })

    def test_review_delete_fail(self):
        client = Client()
        headers  = {'HTTP_Authorization': self.token}
        response = client.delete('/products/1/review/99999', **headers)
        self.assertEqual(response.status_code, 404)