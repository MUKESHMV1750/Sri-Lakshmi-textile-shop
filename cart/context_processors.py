def cart_count(request):
    """Context processor to make cart count available in all templates"""
    count = 0
    if request.user.is_authenticated:
        from .models import Cart
        try:
            cart = Cart.objects.get(user=request.user)
            count = cart.total_items
        except Cart.DoesNotExist:
            pass
    else:
        session_key = request.session.session_key
        if session_key:
            from .models import Cart
            try:
                cart = Cart.objects.get(session_key=session_key)
                count = cart.total_items
            except Cart.DoesNotExist:
                pass
    return {'cart_count': count}
