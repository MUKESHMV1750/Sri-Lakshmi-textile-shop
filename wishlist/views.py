from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Wishlist
from products.models import Product


@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user, product=product
    )
    if not created:
        wishlist_item.delete()
        added = False
    else:
        added = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'added': added,
            'wishlist_count': Wishlist.objects.filter(user=request.user).count(),
        })

    return redirect(request.META.get('HTTP_REFERER', 'shop'))


@login_required
def wishlist_view(request):
    from django.shortcuts import render
    items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'wishlist/wishlist.html', {'items': items, 'wishlist_items': items})


@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True})

    return redirect('wishlist')
