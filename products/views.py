import json, re, bcrypt, jwt

from django.views           import View
from django.http            import JsonResponse
from django.db              import transaction
from django.db.models       import Avg, Count, Q

from products.models        import Product, CustomProduct, ProductOption, Size, Color, FontColor, FontStyle, CustomImage

class ProductView(View):
    def get(self, request, product_id):
        try:
            if not Product.objects.filter(id=product_id).exists():
                return JsonResponse({'MESSAGE':'NOT_EXIST'}, status=404)

            product = Product.objects.annotate(
                avg_score = Avg('review__score'),
                one       = Count('review', filter=Q(review__score=1)),
                two       = Count('review', filter=Q(review__score=2)),
                three     = Count('review', filter=Q(review__score=3)),
                four      = Count('review', filter=Q(review__score=4)),
                five      = Count('review', filter=Q(review__score=5)),
                ).get(id=product_id)

            result = {
                'name'              : product.name,
                'price'             : '{:.0f}'.format(product.price),
                'avg_score'         : product.avg_score,
                'count_rating'      : [{'1' : product.one, '2' :product.two, '3' : product.three, '4' : product.four, '5': product.five}],
                'main_image'        : product.main_image.url,
                'description_image' : product.description_image.url,
                'product_option'    : [{
                    'size_id'       : product_option.size.id,      
                    'size'          : product_option.size.select_size,
                    'color_id'      : product_option.color.id,
                    'color'         : product_option.color.name,
                    'stock'         : product_option.stock,
                    'sales'         : product_option.sales,
                }for product_option in product.productoption_set.all()],
                'cloth_color_image' : [image.image_file.url for image in product.image_set.all()],
                'review'            : [{
                    'user'          : review.user.email,
                    'text'          : review.text,
                    'score'         : review.score,
                    'create_at'     : review.create_at,
                }for review in product.review_set.all()],
            }

            return JsonResponse({'MESSAGE':result}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)