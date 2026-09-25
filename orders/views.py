from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Order, OrderItem
from cart.models import Cart
from accounts.models import Address
from products.models import Coupon


@login_required
def checkout_view(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')

    items = cart.items.select_related('product').all()
    if not items:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')

    addresses = Address.objects.filter(user=request.user)
    coupon_code = request.session.get('coupon_code', '')
    discount = 0

    if coupon_code:
        try:
            coupon = Coupon.objects.get(code=coupon_code)
            if coupon.is_valid:
                if coupon.discount_type == 'percentage':
                    discount = (cart.subtotal * coupon.discount_value) / 100
                    if coupon.maximum_discount:
                        discount = min(discount, coupon.maximum_discount)
                else:
                    discount = coupon.discount_value
        except Coupon.DoesNotExist:
            pass

    shipping = 0 if cart.subtotal >= 999 else 79
    total = cart.subtotal - discount + shipping

    context = {
        'cart': cart,
        'items': items,
        'addresses': addresses,
        'discount': discount,
        'shipping': shipping,
        'total': total,
        'coupon_code': coupon_code,
    }
    return render(request, 'checkout.html', context)


@login_required
def place_order(request):
    if request.method != 'POST':
        return redirect('checkout')

    address_id = request.POST.get('address_id')
    address = None

    if address_id and address_id != 'new':
        try:
            address = Address.objects.get(id=address_id, user=request.user)
        except (Address.DoesNotExist, ValueError):
            pass

    if not address:
        full_name = request.POST.get('full_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        address_line_1 = request.POST.get('address_line_1', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        pincode = request.POST.get('pincode', '').strip()

        if full_name and address_line_1 and city and pincode:
            address = Address.objects.create(
                user=request.user,
                full_name=full_name,
                phone=phone or getattr(request.user, 'phone', ''),
                address_line_1=address_line_1,
                city=city,
                state=state,
                pincode=pincode,
                is_default=True
            )
        else:
            messages.error(request, 'Please select or fill in a valid delivery address.')
            return redirect('checkout')

    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.select_related('product').all()

    if not items:
        messages.error(request, 'Your cart is empty.')
        return redirect('cart')

    # Calculate totals
    subtotal = cart.subtotal
    coupon_code = request.session.get('coupon_code', '')
    discount = 0

    if coupon_code:
        try:
            coupon = Coupon.objects.get(code=coupon_code)
            if coupon.is_valid:
                if coupon.discount_type == 'percentage':
                    discount = (subtotal * coupon.discount_value) / 100
                    if coupon.maximum_discount:
                        discount = min(discount, coupon.maximum_discount)
                else:
                    discount = coupon.discount_value
                coupon.used_count += 1
                coupon.save()
        except Coupon.DoesNotExist:
            pass

    shipping = 0 if subtotal >= 999 else 79
    total = subtotal - discount + shipping

    # Create order
    order = Order.objects.create(
        user=request.user,
        address=address,
        subtotal=subtotal,
        discount=discount,
        shipping_charge=shipping,
        total=total,
        coupon_code=coupon_code,
    )

    # Create order items
    for item in items:
        img = item.product.primary_image
        OrderItem.objects.create(
            order=order,
            product=item.product,
            product_name=item.product.name,
            product_image=img.image.url if img else '',
            quantity=item.quantity,
            price=item.product.effective_price,
            size=item.size,
            color=item.color,
        )
        # Reduce stock
        item.product.stock -= item.quantity
        item.product.save()

    # Clear cart and coupon
    cart.items.all().delete()
    if 'coupon_code' in request.session:
        del request.session['coupon_code']

    # Store order id for payment
    request.session['pending_order_id'] = str(order.id)

    return redirect('payment', order_id=order.id)


@login_required
def order_list_view(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.items.all()
    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'orders/order_detail.html', context)


@login_required
def cancel_order_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status in ['pending', 'confirmed']:
        order.status = 'cancelled'
        order.save()
        # Restore stock
        for item in order.items.all():
            if item.product:
                item.product.stock += item.quantity
                item.product.save()
        messages.success(request, 'Order cancelled successfully.')
    else:
        messages.error(request, 'This order cannot be cancelled.')
    return redirect('order_detail', order_id=order.id)
