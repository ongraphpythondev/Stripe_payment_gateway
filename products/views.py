import json
from django.shortcuts import redirect, render
import stripe
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.views import View
from .models import Product
from .models import Product , Order



stripe.api_key = settings.STRIPE_SECRET_KEY


class CancelView(TemplateView):
    template_name = "products/cancel.html"


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs["pk"]
        product = Product.objects.get(id=product_id)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'inr',
                        'unit_amount': product.price,
                        'product_data': {
                            'name': product.name,
                            # 'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "product_id": product.id
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/buy/' + str(product.id),
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })



class Products(View):
    def get(self , request):
        products = Product.objects.all()
        return render(request , "products/products.html" , {"products":products , "STRIPE_PUBLIC_KEY":settings.STRIPE_PUBLIC_KEY})


class Buy_Product(View):
    def get(self , request , pk):
        product = Product.objects.filter(pk = pk).first()
        order = Order.objects.create(product = product)
        return redirect("order")


class Order_Product(View):
    def get(self , request ):
        orders = Order.objects.all()
        return render(request , "products/order.html" , {"orders": orders})