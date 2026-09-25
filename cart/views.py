from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Cart, CartItem
from products.models import Product, Coupon
import json


def get_or_create_cart(request):
    """Get or create cart for user or session"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart


def cart_view(request):
    cart = get_or_create_cart(request)
    items = cart.items.select_related('product').all()
    context = {
        'cart': cart,
        'items': items,
    }
    return render(request, 'cart.html', context)


def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        size = request.POST.get('size', '')
        color = request.POST.get('color', '')

        product = get_object_or_404(Product, id=product_id, is_active=True)
        cart = get_or_create_cart(request)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            size=size,
            color=color,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'status': 'success',
                'cart_count': cart.total_items,
                'message': f'{product.name} added to cart!'
            })

        messages.success(request, f'{product.name} added to cart!')
        return redirect('cart')

    return redirect('shop')


@require_POST
def update_cart(request):
    item_id = request.POST.get('item_id')
    quantity = int(request.POST.get('quantity', 1))

    cart = get_or_create_cart(request)
    item_total = '0'
    try:
        item = CartItem.objects.get(id=item_id, cart=cart)
        if quantity > 0:
            item.quantity = quantity
            item.save()
            item_total = str(item.total_price)
        else:
            item.delete()
    except CartItem.DoesNotExist:
        pass

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'status': 'success',
            'cart_count': cart.total_items,
            'item_total': item_total,
            'subtotal': str(cart.subtotal),
            'grand_total': str(cart.total),
            'total': str(cart.total),
        })

    return redirect('cart')


def remove_from_cart(request, item_id=None):
    if not item_id and request.method == 'POST':
        item_id = request.POST.get('item_id')

    cart = get_or_create_cart(request)
    if item_id:
        try:
            item = CartItem.objects.get(id=item_id, cart=cart)
            item.delete()
            messages.success(request, 'Item removed from cart.')
        except (CartItem.DoesNotExist, ValueError):
            pass

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'status': 'success',
            'cart_count': cart.total_items,
            'subtotal': str(cart.subtotal),
            'grand_total': str(cart.total),
            'total': str(cart.total),
        })

    return redirect('cart')


@require_POST
def apply_coupon(request):
    code = request.POST.get('coupon_code', '').strip().upper()
    try:
        coupon = Coupon.objects.get(code=code)
        if coupon.is_valid:
            cart = get_or_create_cart(request)
            request.session['coupon_code'] = code
            if coupon.discount_type == 'percentage':
                discount = (cart.subtotal * coupon.discount_value) / 100
                if coupon.maximum_discount:
                    discount = min(discount, coupon.maximum_discount)
            else:
                discount = coupon.discount_value

            grand_total = cart.subtotal - discount if cart.subtotal > discount else 0

            return JsonResponse({
                'success': True,
                'status': 'success',
                'discount': str(discount),
                'subtotal': str(cart.subtotal),
                'grand_total': str(grand_total),
                'total': str(grand_total),
                'message': f'Coupon {code} applied!'
            })
        else:
            return JsonResponse({'success': False, 'status': 'error', 'message': 'Coupon is expired or invalid.'})
    except Coupon.DoesNotExist:
        return JsonResponse({'success': False, 'status': 'error', 'message': 'Invalid coupon code.'})
