import json, unittest, jwt

from django.http        import response
from django.test        import TestCase, Client, client

from carts.models       import Cart
from products.models    import Category, SubCategory, DetailCategory, Product, Size, Color,ProductOption, CustomProduct
from reviews.models     import Review
from users.models       import User
from my_settings        import SECRET_KEY, const_algorithm

class CustomProductViewTest(TestCase):
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
            stock = 100,
            sales = 1000,
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

        headers  = {'HTTP_Authorization': token}
        response = client.post('/product_id/1/custom', json.dumps(product), content_type='application/json', **headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "MESSAGE": "SUCCESS"
        })

    def test_customproduct_no_data_post_fail(self):
        client = Client()
        token = jwt.encode({'id':1}, SECRET_KEY, algorithm=const_algorithm)
        product = {
            'custom_text' : 'testtest'
        }

        headers  = {'HTTP_Authorization': token}
        response = client.post('/product_id/1/custom', json.dumps(product), content_type='application/json', **headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            "MESSAGE": "KEY_ERROR"
        })

class CartViewTest(TestCase):
    @classmethod
    def setUpTestData(self):
        User.objects.bulk_create([
            User(
                email = 'gnsxo9@gmail.com',
                password = 'qweasd123!!!',
                phone_number = '010-1234-1234'
            ),
            User(
                email = 'gnsxo10@gmail.com',
                password = 'qweasd123!!!',
                phone_number = '010-4321-4321'
            )
        ])
        user = User.objects.get(email = 'gnsxo9@gmail.com')
        self.token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm=const_algorithm)


        Category.objects.create(
            name = '반팔'
        )
        Category.objects.create(
            name = '긴팔'
        )

        SubCategory.objects.create(
            option = '프린트',
            category_id = 1,
        )
        SubCategory.objects.bulk_create([
            SubCategory(
                option = '아티스트',
                category_id = 1,
                ),
            SubCategory(
                option = '프린트',
                category_id = 2,
                ),
            SubCategory(
                option = '아티스트',
                category_id = 2,
                )
        ])

        DetailCategory.objects.create(
            detail = '봄',
            sub_category_id = 1,
        )
        DetailCategory.objects.create(
            detail = '김훈태',
            sub_category_id = 2,
        )

        Product.objects.create(
            id = 1,
            name = '프린트봄반팔',
            price = 30000,
            detail_category_id = 1,
            main_image = "https://wecode-23-casetfany.s3.us-east-2.amazonaws.com/mainimage/1-1.jpg"
        )
        Product.objects.create(
            id = 2,
            name = '아티스트훈태반팔',
            price = 100000,
            detail_category_id = 2,
            main_image = "https://wecode-23-casetfany.s3.us-east-2.amazonaws.com/mainimage/1-2.jpg"
        )

        Size.objects.create(
            select_size = 'S'
        )

        Color.objects.create(
            name = 'Red'
        )

        ProductOption.objects.create(
            product_id = 1,
            size_id = 1,
            color_id = 1,
            stock = 10,
            sales = 10
        )
        ProductOption.objects.create(
            product_id = 2,
            size_id = 1,
            color_id = 1,
            stock = 5,
            sales = 5
        )
        CustomProduct.objects.create(
            product_id = 1,
            user_id = 1,
            product_option_id = 1
        )
        Cart.objects.create(
            user_id = 1,
            custom_product_id = 1,
            quantity = 1
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
        CustomProduct.objects.all().delete()
        Cart.objects.all().delete()

    def test_carts_get_success(self):
        self.maxDiff = None
        client = Client()
        token = jwt.encode({'id':1}, SECRET_KEY, algorithm=const_algorithm)
        headers  = {'HTTP_Authorization': token}
        response = client.get('/product_id', **headers)
        self.assertEqual(response.json(),
            {
                'results' : [{
                    "cart_id" : 1,
                    "custom_product_id" : 1,
                    "name" : "프린트봄반팔",
                    "price" : 30000,
                    "size" : 'S',
                    "color" : "Red",
                    "main_image" : 'https://wecode-23-casetfany.s3.us-east-2.amazonaws.com/mainimage/1-1.jpg',
                    "quantity" : 1,
                    "total_price" : 30000,
                }]
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_carts_get_no_cart_fail(self):
        client = Client()
        token = jwt.encode({'id':2}, SECRET_KEY, algorithm=const_algorithm)
        headers  = {'HTTP_Authorization': token}
        response = client.get('/products_id', **headers)
        self.assertEqual(response.status_code, 404)
    
    def test_carts_patch_success(self):
        client = Client()
        headers  = {'HTTP_Authorization': self.token}
        body = {
            "quantity" : -1
        }
        response = client.patch('/product_id/carts/1',body, content_type='application/json', **headers)
        self.assertEqual(response.json(),
            {
                "message": "SUCCESS"
                }
        )
        self.assertEqual(response.status_code, 200)

    def test_carts_patch_invaled_user_fail(self):
        client = Client()
        token = jwt.encode({'id':2}, SECRET_KEY, algorithm=const_algorithm)
        headers  = {'HTTP_Authorization': token}
        body = {
            "quantity" : 1
        }
        response = client.patch('/product_id/carts/1',body,content_type='application/json', **headers)
        self.assertEqual(response.json(),
            {
                "message": "INVALED_USER"
                }
        )
        self.assertEqual(response.status_code, 403)

    def test_carts_delete_success(self):
        client = Client()
        token = jwt.encode({'id':1}, SECRET_KEY, algorithm=const_algorithm)
        headers  = {'HTTP_Authorization': token}
        response = client.delete('/product_id/carts/1', **headers)
        self.assertEqual(response.json(),
            {
                "message": "SUCCESS"
                }
        )
        self.assertEqual(response.status_code, 200)

    def test_carts_delete_not_found_fail(self):
        client = Client()
        headers  = {'HTTP_Authorization': self.token}
        response = client.delete('/product_id/carts/2', **headers)
        self.assertEqual(response.json(),
            {
                "message": "NOT_FOUND"
                }
        )
        self.assertEqual(response.status_code, 404)

