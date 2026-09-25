from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Review
from products.models import Product


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if Review.objects.filter(product=product, user=request.user).exists():
        messages.warning(request, 'You have already reviewed this product.')
        return redirect('product_detail', slug=product.slug)

    if request.method == 'POST':
        rating = int(request.POST.get('rating', 5))
        title = request.POST.get('title', '')
        comment = request.POST.get('comment', '')

        Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            title=title,
            comment=comment,
        )
        messages.success(request, 'Thank you for your review!')
        return redirect('product_detail', slug=product.slug)

    return redirect('product_detail', slug=product.slug)


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    product_slug = review.product.slug
    review.delete()
    messages.success(request, 'Review deleted.')
    return redirect('product_detail', slug=product_slug)
