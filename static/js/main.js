/**
 * LoomLuxe - Main Application JavaScript
 * Global Toast Notifications, Sticky Header, Mobile Menu, Wishlist & Search
 */

document.addEventListener('DOMContentLoaded', function () {
    initHeader();
    initMobileMenu();
    initWishlistButtons();
    initQuickView();
});

// Header scroll effect
function initHeader() {
    const navbar = document.querySelector('header');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('shadow-md');
            } else {
                navbar.classList.remove('shadow-md');
            }
        });
    }
}

// Mobile navigation toggle
function initMobileMenu() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-links');
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            navToggle.classList.toggle('open');
        });
    }
}

// Toast notification helper
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    const toastMsg = document.getElementById('toast-msg');
    if (toast && toastMsg) {
        toastMsg.textContent = message;
        const icon = toast.querySelector('i');
        if (icon) {
            icon.className = type === 'success' ? 'fa-solid fa-circle-check text-emerald-400' :
                             type === 'error' ? 'fa-solid fa-triangle-exclamation text-red-400' :
                             'fa-solid fa-circle-info text-blue-400';
        }
        toast.classList.remove('translate-y-20', 'opacity-0');
        toast.classList.add('translate-y-0', 'opacity-100');
        setTimeout(() => {
            toast.classList.remove('translate-y-0', 'opacity-100');
            toast.classList.add('translate-y-20', 'opacity-0');
        }, 3000);
    } else {
        let container = document.querySelector('.toast-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'toast-container fixed bottom-5 right-5 z-50 space-y-2';
            document.body.appendChild(container);
        }

        const t = document.createElement('div');
        t.className = `toast toast-${type} bg-black text-white px-6 py-3.5 rounded-2xl shadow-xl flex items-center space-x-3 text-sm transition-all duration-300`;
        const iconClass = type === 'success' ? 'fa-circle-check text-emerald-400' :
                          type === 'error' ? 'fa-triangle-exclamation text-red-400' :
                          'fa-circle-info text-blue-400';
        t.innerHTML = `
            <i class="fa-solid ${iconClass}"></i>
            <span>${message}</span>
            <button class="ml-4 text-gray-400 hover:text-white" onclick="this.parentElement.remove()">&times;</button>
        `;

        container.appendChild(t);

        setTimeout(() => {
            t.style.opacity = '0';
            setTimeout(() => t.remove(), 400);
        }, 3500);
    }
}

// Global Add to Cart helper
function addToCart(productId, quantity = 1, size = '', color = '') {
    if (!productId) return;

    fetch('/cart/add/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCsrfToken(),
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: `product_id=${productId}&quantity=${quantity}&size=${encodeURIComponent(size)}&color=${encodeURIComponent(color)}`
    })
    .then(res => {
        if (!res.ok) throw new Error('Network error');
        return res.json();
    })
    .then(data => {
        if (data.success || data.status === 'success') {
            showToast(data.message || 'Added to cart!', 'success');
            if (data.cart_count !== undefined) {
                updateBadge('#cartBadge, .cart-count', data.cart_count);
            }
        } else {
            showToast(data.message || 'Failed to add item to cart', 'error');
        }
    })
    .catch(err => {
        console.error(err);
        showToast('Could not add item to cart. Please try again.', 'error');
    });
}

// Global Toggle Wishlist helper
function toggleWishlist(productId) {
    if (!productId) return;

    fetch(`/wishlist/toggle/${productId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCsrfToken(),
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(res => {
        if (res.redirected) {
            window.location.href = res.url;
            return null;
        }
        return res.json();
    })
    .then(data => {
        if (!data) return;
        if (data.success || data.status === 'added' || data.status === 'removed') {
            const isAdded = data.added || data.status === 'added';
            const msg = isAdded ? 'Added to wishlist!' : 'Removed from wishlist';
            showToast(msg, isAdded ? 'success' : 'info');

            // Update heart icon states
            const selectors = `[onclick*="toggleWishlist('${productId}')"], .wishlist-btn[data-product-id="${productId}"]`;
            document.querySelectorAll(selectors).forEach(btn => {
                const icon = btn.querySelector('i');
                if (icon) {
                    if (isAdded) {
                        icon.className = 'fa-solid fa-heart text-red-500';
                    } else {
                        icon.className = 'fa-regular fa-heart text-gray-700';
                    }
                }
            });

            if (data.wishlist_count !== undefined) {
                updateBadge('#wishlist-badge, .wishlist-count', data.wishlist_count);
            }
        } else if (data.redirect) {
            window.location.href = data.redirect;
        } else {
            showToast(data.message || 'Could not update wishlist', 'error');
        }
    })
    .catch(err => {
        console.error(err);
        showToast('Please log in to manage your wishlist', 'error');
    });
}

// Wishlist toggle handler via delegate
function initWishlistButtons() {
    document.body.addEventListener('click', function (e) {
        const btn = e.target.closest('.wishlist-btn');
        if (!btn) return;
        
        e.preventDefault();
        const productId = btn.dataset.productId;
        if (productId) {
            toggleWishlist(productId);
        }
    });
}

// Quick View Modal
function initQuickView() {
    document.body.addEventListener('click', function (e) {
        const btn = e.target.closest('.quickview-btn');
        if (!btn) return;

        e.preventDefault();
        const productId = btn.dataset.productId;
        if (!productId) return;

        fetch(`/products/${productId}/quick-view/`)
            .then(res => res.json())
            .then(data => {
                showQuickViewModal(data);
            })
            .catch(err => {
                showToast('Failed to load product preview', 'error');
            });
    });
}

function showQuickViewModal(data) {
    let modal = document.getElementById('quickview-modal');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'quickview-modal';
        modal.className = 'modal-backdrop';
        document.body.appendChild(modal);
    }

    modal.innerHTML = `
        <div class="modal-content glass-card animate-zoom">
            <button class="modal-close" onclick="closeQuickViewModal()">&times;</button>
            <div class="modal-body product-quickview-grid">
                <div class="modal-image">
                    <img src="${data.primary_image || 'https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=600'}" alt="${data.name}">
                </div>
                <div class="modal-details">
                    <span class="badge bg-gold">${data.category}</span>
                    <h2>${data.name}</h2>
                    <div class="price-box">
                        <span class="price-current">₹${data.price}</span>
                        ${data.old_price ? `<span class="price-old">₹${data.old_price}</span>` : ''}
                    </div>
                    <p class="description">${data.description || ''}</p>
                    <div class="modal-actions">
                        <button class="btn btn-primary add-to-cart-btn" onclick="addToCart('${data.id}')">
                            <i class="fas fa-shopping-bag"></i> Add to Cart
                        </button>
                        <a href="/products/${data.slug}/" class="btn btn-outline">View Details</a>
                    </div>
                </div>
            </div>
        </div>
    `;

    modal.style.display = 'flex';
}

function closeQuickViewModal() {
    const modal = document.getElementById('quickview-modal');
    if (modal) modal.style.display = 'none';
}

// CSRF Helper
function getCsrfToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, 10) === ('csrftoken' + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(10));
                break;
            }
        }
    }
    return cookieValue || document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
}

// Badge updater helper
function updateBadge(selector, count) {
    const badges = document.querySelectorAll(selector);
    badges.forEach(badge => {
        badge.textContent = count;
        if (count > 0) {
            badge.style.display = 'inline-flex';
        } else {
            badge.style.display = 'none';
        }
    });
}

