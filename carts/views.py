import json, re, bcrypt, jwt

from django.views           import View
from django.http            import JsonResponse
from django.db              import transaction
from django.db.models       import Q, Sum, F

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

class CartView(View):
    @LoginDecorator
    def get(self, request):
        carts = Cart.objects.filter(user = request.user)
        
        results=[{
            "cart_id"           : cart.id,
            "custom_product_id" : cart.custom_product.id,
            "name"              : cart.custom_product.product.name,
            "price"             : round(cart.custom_product.product.price),
            "size"              : cart.custom_product.product_option.size.select_size,
            "color"             : cart.custom_product.product_option.color.name,
            "main_image"        : cart.custom_product.product.main_image,
            "quantity"          : cart.quantity,
            "total_price"       : round(cart.custom_product.product.price) * cart.quantity,
        }for cart in carts]

        final_total_price = carts.aggregate(price = Sum(F("quantity") * F("custom_product__product__price")))["price"] or 0

        return JsonResponse({'results': results , 'final_total_price': round(final_total_price)}, status=200)
    
    @LoginDecorator
    @transaction.atomic
    def patch(self,request,cart_id):
        data   = json.loads(request.body)
        cart   = Cart.objects.get(id=cart_id, user = request.user)
        product_option = cart.custom_product.product_option

        if product_option.stock < cart.quantity + data['quantity']:
            return JsonResponse({'message':'OUT_OF_STOCK'},status = 400)
        
        cart.quantity += data['quantity']
        cart.save()

        product_option.stock -= data['quantity']
        product_option.sales += data['quantity']
        product_option.save()

        return JsonResponse({'message':'SUCCESS'}, status = 200)

    @LoginDecorator
    @transaction.atomic
    def delete(self,request,cart_id):
        if not Cart.objects.filter(id = cart_id, user = request.user).exists():
            return JsonResponse({'message': 'NOT_FOUND'}, status = 404)

        cart           = Cart.objects.get(id=cart_id, user = request.user)
        product_option = cart.custom_product.product_option
        custom_product = cart.custom_product

        product_option.stock += cart.quantity
        product_option.sales -= cart.quantity
        product_option.save()
        cart.delete()
        custom_product.delete()

        return JsonResponse({'message': 'SUCCESS'}, status = 200)