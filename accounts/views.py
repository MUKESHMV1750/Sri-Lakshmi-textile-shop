from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import RegisterForm, LoginForm, ProfileForm, AddressForm
from .models import User, Address
from orders.models import Order


def register_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('admin_dashboard')
        return redirect('home')

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        context = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
        }

        # Validations
        if not email or not password:
            messages.error(request, 'Please enter both an email address and a password.')
            return render(request, 'register.html', context)

        if confirm_password and password != confirm_password:
            messages.error(request, 'Passwords do not match. Please try again.')
            return render(request, 'register.html', context)

        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return render(request, 'register.html', context)

        if User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email address already exists. Please sign in.')
            return render(request, 'register.html', context)

        # Generate unique username from email
        base_username = email.split('@')[0]
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}_{counter}"
            counter += 1

        # Create user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone=phone
            )

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'Account created successfully! Welcome to LoomLuxe, {first_name or username}.')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'Could not create account: {str(e)}')
            return render(request, 'register.html', context)

    return render(request, 'register.html')


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('admin_dashboard')
        return redirect('home')

    if request.method == 'POST':
        login_id = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not login_id or not password:
            messages.error(request, 'Please enter both email/username and password.')
            return render(request, 'login.html', {'login_id': login_id})

        # Find user by email or username
        user_obj = User.objects.filter(email__iexact=login_id).first() or User.objects.filter(username__iexact=login_id).first()

        user = None
        if user_obj:
            user = authenticate(request, username=user_obj.username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next') or request.POST.get('next')

            if user.is_staff or user.is_superuser:
                messages.success(request, f'Logged in successfully as Admin! Welcome back, {user.get_full_name() or user.username}.')
                return redirect(next_url or 'admin_dashboard')
            else:
                messages.success(request, f'Logged in successfully! Welcome back, {user.get_full_name() or user.username}.')
                return redirect(next_url or 'home')
        else:
            messages.error(request, 'Invalid email/username or password. Please try again.')
            return render(request, 'login.html', {'login_id': login_id})

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def dashboard_view(request):
    orders = Order.objects.filter(user=request.user)[:5]
    addresses = Address.objects.filter(user=request.user)
    context = {
        'orders': orders,
        'addresses': addresses,
        'total_orders': Order.objects.filter(user=request.user).count(),
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def addresses_view(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'accounts/addresses.html', {'addresses': addresses})


@login_required
def add_address_view(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, 'Address added successfully!')
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('addresses')
    else:
        form = AddressForm()
    return render(request, 'accounts/add_address.html', {'form': form})


@login_required
def edit_address_view(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address updated!')
            return redirect('addresses')
    else:
        form = AddressForm(instance=address)
    return render(request, 'accounts/edit_address.html', {'form': form, 'address': address})


@login_required
def delete_address_view(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    address.delete()
    messages.success(request, 'Address deleted.')
    return redirect('addresses')
