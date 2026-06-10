import stripe
from django.conf import settings
from users.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_product(course):
    product = stripe.Product.create(
        name=course.title,
        description=course.description,
    )
    return product['id']

def create_stripe_price(amount, product_id):
    price = stripe.Price.create(
        unit_amount=int(amount * 100),  # в копейках
        currency='rub',
        product=product_id,
    )
    return price['id']

def create_checkout_session(price_id, success_url, cancel_url):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session['id'], session['url']

def create_payment_session(course, user, success_url, cancel_url):
    product_id = create_stripe_product(course)
    price_id = create_stripe_price(course.price, product_id)
    session_id, session_url = create_checkout_session(price_id, success_url, cancel_url)

    Payment.objects.create(
        user=user,
        paid_course=course,
        amount=course.price,
        payment_method='card',
        stripe_session_id=session_id,
        stripe_payment_status='pending',
    )
    return session_url