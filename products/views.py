from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from .models import Product, Category, Banner


def home_view(request):
    categories = Category.objects.filter(is_active=True, parent__isnull=True)[:9]
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    bestsellers = Product.objects.filter(is_active=True, is_bestseller=True)[:8]
    new_arrivals = Product.objects.filter(is_active=True, is_new_arrival=True)[:8]
    sale_products = Product.objects.filter(is_active=True, sale_price__isnull=False)[:4]

    hero_banners = list(Banner.objects.filter(is_active=True).order_by('display_order', '-created_at'))
    if not hero_banners:
        Banner.objects.create(
            title="LoomLuxe Sport & Heritage Project",
            subtitle="Introducing our latest collection, designed specifically for textile connoisseurs. Features handwoven pure silk, organic handblock cottons, and technical apparel with bold craftsmanship.",
            badge="New Collection 2026",
            image_url_override="https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&q=80&w=1800",
            link_url="/shop/",
            button_text="Shop Now",
            display_order=1
        )
        Banner.objects.create(
            title="Royal Kanjeevaram & Banarasi Silk",
            subtitle="Embrace timeless elegance with our handwoven pure Mulberry silk sarees, zardosi borders, and intricate heritage weaves crafted by master artisans.",
            badge="Handcrafted Heritage",
            image_url_override="https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&q=80&w=1800",
            link_url="/shop/?category=silk-sarees",
            button_text="Explore Silk Sarees",
            display_order=2
        )
        Banner.objects.create(
            title="Organic Handblock Cottons & Linens",
            subtitle="Breathable everyday luxury tailored from pure organic cotton and unbleached linen with traditional indigo block prints and modern silhouettes.",
            badge="Sustainable Luxury",
            image_url_override="https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?auto=format&fit=crop&q=80&w=1800",
            link_url="/shop/?category=cotton-fabrics",
            button_text="Shop Cotton Fabrics",
            display_order=3
        )
        hero_banners = list(Banner.objects.filter(is_active=True).order_by('display_order', '-created_at'))

    context = {
        'categories': categories,
        'featured_products': featured_products,
        'bestsellers': bestsellers,
        'new_arrivals': new_arrivals,
        'sale_products': sale_products,
        'hero_banners': hero_banners,
    }
    return render(request, 'home.html', context)


def shop_view(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True, parent__isnull=True)

    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(Q(category=category) | Q(category__parent=category))

    # Price filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Color filter
    color = request.GET.get('color')
    if color:
        products = products.filter(color__icontains=color)

    # Size filter
    size = request.GET.get('size')
    if size:
        products = products.filter(available_sizes__contains=[size])

    # Search
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query) |
            Q(fabric__icontains=search_query) |
            Q(brand__icontains=search_query)
        )

    # Sorting
    sort = request.GET.get('sort', 'newest')
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'name_az':
        products = products.order_by('name')
    elif sort == 'popular':
        products = products.order_by('-views_count')
    else:
        products = products.order_by('-created_at')

    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    context = {
        'products': products,
        'categories': categories,
        'current_category': category_slug,
        'search_query': search_query or '',
        'current_sort': sort,
    }
    return render(request, 'shop.html', context)


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    product.views_count += 1
    product.save(update_fields=['views_count'])

    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(id=product.id)[:4]

    from reviews.models import Review
    reviews = Review.objects.filter(product=product, is_approved=True)
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'review_count': reviews.count(),
    }
    return render(request, 'product.html', context)


def search_suggestions(request):
    """AJAX endpoint for live search"""
    query = request.GET.get('q', '')
    if len(query) >= 2:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(category__name__icontains=query),
            is_active=True
        )[:5]
        results = []
        for p in products:
            img = p.primary_image
            results.append({
                'name': p.name,
                'slug': p.slug,
                'price': str(p.effective_price),
                'image': img.image_url if img else '',
            })
        return JsonResponse({'results': results})
    return JsonResponse({'results': []})


def about_view(request):
    return render(request, 'about.html')


def contact_view(request):
    if request.method == 'POST':
        from django.contrib import messages
        messages.success(request, 'Thank you for your message! We will get back to you shortly.')
        return render(request, 'contact.html')
    return render(request, 'contact.html')
