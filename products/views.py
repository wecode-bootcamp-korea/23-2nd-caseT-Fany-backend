import json

from django.views           import View
from django.http            import JsonResponse
from django.db              import transaction
from django.db.models       import Avg, Count, Q, Sum

from products.models        import Product, CustomProduct, ProductOption, Size, Color, FontColor, FontStyle, CustomImage
from carts.models           import Cart

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
                'main_image'        : product.main_image,
                'description_image' : product.description_image,
                'product_option'    : [{
                    'size_id'       : product_option.size.id,      
                    'size'          : product_option.size.select_size,
                    'color_id'      : product_option.color.id,
                    'color'         : product_option.color.name,
                    'stock'         : product_option.stock,
                    'sales'         : product_option.sales,
                }for product_option in product.productoption_set.all()],
                'cloth_color_image' : [image.image_file for image in product.image_set.all()],
                'review'            : [{
                    'user'          : review.user.email,
                    'text'          : review.text,
                    'score'         : review.score,
                    'create_at'     : review.create_at,
                    'image'         : review.image,
                }for review in product.review_set.all()],
            }

            return JsonResponse({'MESSAGE':result}, status=200)
            
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)

class ProductsView(View):
    def get(self,request):
        category        = request.GET.get('category',None)
        sub_category    = request.GET.get('sub_category',None)
        detail_category = request.GET.getlist('detail_category',None)
        color           = request.GET.getlist('color',None)
        sorting         = request.GET.get('sorting',None)
        search          = request.GET.get('KeyWord',None)
        limit           = request.GET.get('limit',None)
        offset          = int(request.GET.get('offset',0))
    
        filters = Q()

        if category :
            filters &= Q(detail_category__sub_category__category = category) 

        if sub_category :
            filters &= Q(detail_category__sub_category = sub_category)

        if detail_category :
            filters &= Q(detail_category_in = detail_category)
        
        if color :
            filters &= Q(productoption__color__in = color)

        if search :
            filters = (Q(name__icontains = search)|
                Q(detail_category__detail__icontains = search)|
                Q(detail_category__sub_category__option__icontains = search)|
                Q(detail_category__sub_category__category__name__icontains = search)
                )
        
        sort_name = {
            'new'        : '-create_at',
            'bestseller' : '-sales',
        }

        if limit:
            limit = offset + int(limit)

        products = Product.objects.filter(filters)\
                                  .annotate(sales = Sum('productoption__sales'))\
                                  .order_by(sort_name.get(sorting,'id'))[offset:limit]

        results = [{
            'id'           : product.id,
            'name'         : product.name,
            'price'        : round(product.price),
            'main_image'   : product.main_image,
            'sales'        : product.sales,
            'category'     : product.detail_category.sub_category.category.name,
            'sub_category' : product.detail_category.sub_category.option,
            'detail'       : product.detail_category.detail,
            }for product in products]
    
        return JsonResponse({'results' : results}, status = 200)
