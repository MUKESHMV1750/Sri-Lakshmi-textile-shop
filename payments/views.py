import razorpay
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Payment
from orders.models import Order


@login_required
def payment_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if hasattr(order, 'payment') and order.payment.status == 'completed':
        return redirect('order_detail', order_id=order.id)

    # Create Razorpay order
    razorpay_order = None
    razorpay_key = settings.RAZORPAY_KEY_ID

    if razorpay_key:
        try:
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            amount = int(order.total * 100)  # Amount in paise
            razorpay_order = client.order.create({
                'amount': amount,
                'currency': 'INR',
                'payment_capture': 1
            })

            # Create payment record
            payment, created = Payment.objects.get_or_create(
                order=order,
                defaults={
                    'user': request.user,
                    'amount': order.total,
                    'razorpay_order_id': razorpay_order['id'],
                }
            )
            if not created:
                payment.razorpay_order_id = razorpay_order['id']
                payment.save()
        except Exception as e:
            messages.error(request, f'Payment gateway error. Please try again.')

    context = {
        'order': order,
        'razorpay_key': razorpay_key,
        'razorpay_order': razorpay_order,
    }
    return render(request, 'payments/payment.html', context)


@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        try:
            razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            razorpay_signature = request.POST.get('razorpay_signature', '')

            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

            # Verify signature
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature,
            }
            client.utility.verify_payment_signature(params_dict)

            # Update payment
            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
            payment.razorpay_payment_id = razorpay_payment_id
            payment.razorpay_signature = razorpay_signature
            payment.status = 'completed'
            payment.save()

            # Update order
            payment.order.status = 'confirmed'
            payment.order.save()

            return redirect('payment_success', order_id=payment.order.id)

        except Exception as e:
            return redirect('payment_failed')

    return redirect('home')


@login_required
def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'payments/success.html', {'order': order})


def payment_failed(request):
    return render(request, 'payments/failed.html')
