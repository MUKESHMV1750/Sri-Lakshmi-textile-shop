from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Return, ReturnImage
from orders.models import Order, OrderItem


@login_required
def request_return(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status != 'delivered':
        messages.error(request, 'Returns can only be requested for delivered orders.')
        return redirect('order_detail', order_id=order.id)

    items = order.items.all()

    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        return_type = request.POST.get('return_type')
        reason = request.POST.get('reason')
        description = request.POST.get('description', '')

        order_item = get_object_or_404(OrderItem, id=item_id, order=order)

        return_request = Return.objects.create(
            order=order,
            order_item=order_item,
            user=request.user,
            return_type=return_type,
            reason=reason,
            description=description,
        )

        # Handle image uploads
        images = request.FILES.getlist('images')
        for image in images:
            ReturnImage.objects.create(
                return_request=return_request,
                image=image,
            )

        messages.success(request, 'Return request submitted successfully!')
        return redirect('return_status', return_id=return_request.id)

    return render(request, 'returns/request_return.html', {'order': order, 'items': items})


@login_required
def return_list(request):
    returns = Return.objects.filter(user=request.user)
    return render(request, 'returns/return_list.html', {'returns': returns})


@login_required
def return_status(request, return_id):
    return_request = get_object_or_404(Return, id=return_id, user=request.user)
    images = return_request.images.all()
    return render(request, 'returns/return_status.html', {
        'return_request': return_request,
        'images': images,
    })
