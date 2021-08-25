import json, re, bcrypt, jwt

from django.views           import View
from django.http            import JsonResponse
from django.db              import transaction
from django.db.models       import Q

from products.models        import Product,ProductOption, Size, Color, CustomImage, CustomProduct, FontColor, FontStyle
from carts.models           import Cart
from users.utils            import LoginDecorator

class CustomProductView(View):
    @LoginDecorator
    @transaction.atomic
    def post(self, request, product_id):
        try:
            user       = request.user
            data       = json.loads(request.body)

            product_option = ProductOption.objects.get(
                product_id = product_id, 
                size       = data['size_id'],
                color      = data['color_id'],
            )

            if not product_option.stock:
                return JsonResponse({'MESSAGE':'OUT_OF_STOCK'}, status = 400)
        
            product_option.stock -= 1
            product_option.sales += 1
            product_option.save()

            q = Q(user_id = user.id) & Q(product_id = product_id)
            
            customproduct, custom_is_created = CustomProduct.objects.get_or_create(
                user_id           = user.id,
                product_id        = product_id,
                font_color_id     = data.get('font_color_id'),
                font_style_id     = data.get('font_style_id'),
                custom_image_id   = data.get('custom_image_id'),
                custom_text       = data.get('custom_text'),
                coordinate_x      = data.get('coordinate_x'),
                coordinate_y      = data.get('coordinate_y'),
                product_option_id = product_option.id,
            )

            cart_product, cart_is_created = Cart.objects.get_or_create(user_id = user.id, custom_product_id = customproduct.id, defaults={'quantity' : 1 })
            if not cart_is_created:
                cart_product.quantity += 1
                cart_product.save()

                return JsonResponse({'MESSAGE':'QUANTITY_ADD'}, status = 200)
                
            return JsonResponse({'MESSAGE':'SUCCESS'}, status = 200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)