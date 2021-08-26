import json, boto3, uuid

from django.views    import View
from django.http     import JsonResponse
from django.db       import transaction

from reviews.models  import Review
from products.models import Product
from users.utils     import LoginDecorator
from my_settings     import AWS_S3_ACCESS_KEY_ID, AWS_S3_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME

class ReviewView(View):
    @transaction.atomic
    @LoginDecorator
    def post(self, request, product_id):
        try:
            review, is_created = Review.objects.get_or_create(
                    user_id    = request.user.id,
                    product_id = product_id,
                    defaults   = {'score' : 0 }
                )
            
            text  = request.POST.get('text', review.text)
            score = request.POST.get('score', review.score)
            image = request.FILES.get('image')

            if is_created or image:
                upload_key = str(uuid.uuid4()) + image.name if not review.key else review.key

                s3_resource  = boto3.resource(
                    's3',
                    aws_access_key_id     = AWS_S3_ACCESS_KEY_ID,
                    aws_secret_access_key = AWS_S3_SECRET_ACCESS_KEY,
                )
                bucket = s3_resource.Bucket(name = AWS_STORAGE_BUCKET_NAME)

                bucket.upload_fileobj(
                image,
                upload_key,
                ExtraArgs = {
                    'ContentType' : image.content_type
                }
                )
                
                review.image_url = 'https://wecode-23-casetfany.s3.us-east-2.amazonaws.com/' + upload_key if image else None
                review.key       = upload_key
            
            review.text = text 
            review.score= score
            review.save()

            result = {
                'user'         : request.user.id,
                'product_id'   : review.product_id,
                'product_name' : review.product.name,
                'score'        : review.score,
                'text'         : review.text,
                'image_url'    : review.image_url,
            }

            return JsonResponse({'MESSAGE':result},status = 201)
    
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

    @LoginDecorator
    def get(self, request, product_id, review_id): 
        try:
            user      = request.user.id

            if not Review.objects.filter(id=review_id, user_id = user).exists():
                return JsonResponse({'MESSAGE':'NOT_EXISTS'}, status=404)

            review = Review.objects.get(id = review_id)
            result = {
                'user'         : user,
                'product_id'   : review.product_id,
                'product_name' : review.product.name,
                'score'        : review.score,
                'text'         : review.text,
                'image_url'    : review.image_url,
            }

            return JsonResponse({'MESSAGE':result}, status = 200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

    @LoginDecorator
    def delete(self, request, product_id, review_id):
        user       = request.user.id

        if not Review.objects.filter(id=review_id, user_id=user).exists():
            return JsonResponse({'MESSAGE':'NOT_EXISTS'}, status=404)
        
        review = Review.objects.get(id=review_id, user_id=user) 

        if review.image_url:
            s3_resource  = boto3.resource(
                        's3',
                        aws_access_key_id     = AWS_S3_ACCESS_KEY_ID,
                        aws_secret_access_key = AWS_S3_SECRET_ACCESS_KEY,
                    )
            bucket = s3_resource.Bucket(name = AWS_STORAGE_BUCKET_NAME)
            bucket.delete_objects(key = review.key)

        review.delete() 

        return JsonResponse({"MESSAGE": 'SUCCESS'}, status=200)
