import json, unittest

# Create your tests here.
from django.http import response
from django.test import TestCase, Client, client

from products.models import Category,SubCategory,DetailCategory,Product,Size,Color,ProductOption

class ProductsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):

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

    def tearDown(self):
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        DetailCategory.objects.all().delete()
        Product.objects.all().delete()
        Size.objects.all().delete()
        Color.objects.all().delete()
        ProductOption.objects.all().delete()

    def test_listview_get_success(self):
        self.maxDiff = None
        client = Client()
        response = client.get('/products?category=1&sub_category=1&detail_category=1')
        self.assertEqual(response.json(),
            {
                'results' : [{
                    "id" : 1,
                    "name" : "프린트봄반팔",
                    "price" : 30000,
                    "main_image" : 'https://wecode-23-casetfany.s3.us-east-2.amazonaws.com/mainimage/1-1.jpg',
                    "sales" : 10,
                    "category" : "반팔",
                    "sub_category" : "프린트",               
                    "detail" : "봄",
                }]
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_listview_get_empty_success(self):
        client = Client()
        response = client.get('/products?category=2&sub_category=2')
        self.assertEqual(response.json(),
            {
                "results" : []
                }
        )
        self.assertEqual(response.status_code, 200)