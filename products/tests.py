import json, unittest, jwt

from django.http import response
from django.test import TestCase, Client

from products.models import *
from reviews.models import Review
from users.models import User
from my_settings import SECRET_KEY, const_algorithm

class ProductViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            email = 'wecode12@wecode.com',
            password = 'wecode12#',
            phone_number = '010-3333-3333'
        )

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
            stock = 5,
            sales = 10,
        )

        Review.objects.create(
            user_id = 1,
            text = 'testtesttest',
            product_id = 1,
            score = 5,
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

    def test_customproduct_post_success(self):
        client = Client()
        token = jwt.encode({'id':1}, SECRET_KEY, algorithm=const_algorithm)
        product = {
            'size_id' : 1,
            'color_id' : 1
        }

        headers  = {'HTTP_Authoriazation': token}
        response = client.post('/products/1/custom', json.dumps(product), content_type='application/json', **headers)
        self.assertEqual(response.status_code, 200)

    def test_customproduct_no_data_post_fail(self):
        client = Client()

        response = client.get('/products?product_id=9999')
        self.assertEqual(response.status_code, 400)
