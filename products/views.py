import json, re, bcrypt, jwt
from django.core.checks.messages import Error

from django.views           import View
from django.http            import JsonResponse
from django.db              import transaction
from django.db.models       import Avg, Count, Q

from products.models        import Product, CustomProduct, ProductOption, Size, Color, FontColor, FontStyle, CustomImage
from carts.models           import Cart
from users.utils            import login_decorator

class ProductView(View):
    def get(self, request):
        try:
            product_id = request.GET.get('product_id')

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
                'main_image'        : str(product.main_image),
                'description_image' : str(product.description_image),
                'product_option'    : [{
                    'size'          : product_option.size.select_size,
                    'color'         : product_option.color.name,
                    'stock'         : product_option.stock,
                    'sales'         : product_option.sales,
                }for product_option in product.productoption_set.all()],
                'cloth_color_image' : [str(image.image_file) for image in product.image_set.all()],
                'review'            : [{
                    'user'          : review.user.email,
                    'text'          : review.text,
                    'score'         : review.score,
                    'create_at'        : review.create_at,
                }for review in product.review_set.all()],
            }

            return JsonResponse({'MESSAGE':result}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)
