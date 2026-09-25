/**
 * LoomLuxe - Shopping Cart JavaScript
 * Interactive cart updates, AJAX add-to-cart, quantity adjustments & coupon application
 */

document.addEventListener('DOMContentLoaded', function () {
    initAddToCart();
    initQuantityControls();
    initCouponForm();
});

// Global Add to Cart Delegation
function initAddToCart() {
    document.body.addEventListener('click', function (e) {
        const btn = e.target.closest('.add-to-cart-btn');
        if (!btn) return;

        e.preventDefault();
        const productId = btn.dataset.productId;
        const sizeInput = document.querySelector('input[name="selected_size"]:checked') || document.querySelector('#selected-size');
        const colorInput = document.querySelector('input[name="selected_color"]:checked') || document.querySelector('#selected-color');
        const qtyInput = document.querySelector('#product-qty') || document.querySelector('.qty-input');

        const size = sizeInput ? sizeInput.value : '';
        const color = colorInput ? colorInput.value : '';
        const quantity = qtyInput ? parseInt(qtyInput.value) || 1 : 1;

        if (!productId) return;

        const originalText = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Adding...';

        fetch('/cart/add/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCsrfToken()
            },
            body: `product_id=${productId}&quantity=${quantity}&size=${encodeURIComponent(size)}&color=${encodeURIComponent(color)}`
        })
        .then(res => res.json())
        .then(data => {
            btn.disabled = false;
            btn.innerHTML = originalText;

            if (data.success || data.status === 'success') {
                showToast(data.message || 'Added to cart!', 'success');
                if (data.cart_count !== undefined) {
                    updateBadge('#cartBadge, .cart-count', data.cart_count);
                }
            } else {
                showToast(data.message || 'Failed to add item', 'error');
            }
        })
        .catch(err => {
            btn.disabled = false;
            btn.innerHTML = originalText;
            showToast('Something went wrong. Please try again.', 'error');
        });
    });
}

// Cart Quantity Controls (+ / - and removal)
function initQuantityControls() {
    const cartContainer = document.querySelector('.cart-section');
    if (!cartContainer) return;

    cartContainer.addEventListener('click', function (e) {
        // Quantity Plus / Minus buttons
        const qtyBtn = e.target.closest('.qty-btn');
        if (qtyBtn) {
            const itemId = qtyBtn.dataset.itemId;
            const input = qtyBtn.parentElement.querySelector('.cart-qty-input');
            let currentQty = parseInt(input.value) || 1;

            if (qtyBtn.classList.contains('qty-plus')) {
                currentQty += 1;
            } else if (qtyBtn.classList.contains('qty-minus') && currentQty > 1) {
                currentQty -= 1;
            }

            input.value = currentQty;
            updateCartItem(itemId, currentQty);
            return;
        }

        // Remove item button
        const removeBtn = e.target.closest('.remove-cart-item');
        if (removeBtn) {
            e.preventDefault();
            const itemId = removeBtn.dataset.itemId;
            removeCartItem(itemId);
        }
    });

    // Quantity Direct Change Input
    cartContainer.addEventListener('change', function (e) {
        if (e.target.classList.contains('cart-qty-input')) {
            const itemId = e.target.dataset.itemId;
            let qty = parseInt(e.target.value) || 1;
            if (qty < 1) qty = 1;
            e.target.value = qty;
            updateCartItem(itemId, qty);
        }
    });
}

// Update Cart Item Quantity AJAX
function updateCartItem(itemId, quantity) {
    fetch('/cart/update/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCsrfToken()
        },
        body: `item_id=${itemId}&quantity=${quantity}`
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'success') {
            // Update row item total
            const itemRow = document.querySelector(`.cart-item-row[data-item-id="${itemId}"]`);
            if (itemRow && data.item_total !== undefined) {
                const itemTotalElem = itemRow.querySelector('.cart-item-total');
                if (itemTotalElem) itemTotalElem.textContent = `₹${data.item_total}`;
            }

            // Update cart summary totals
            updateCartSummary(data);
            showToast('Cart updated', 'info');
        } else {
            showToast(data.message || 'Failed to update quantity', 'error');
        }
    })
    .catch(err => {
        showToast('Error updating cart', 'error');
    });
}

// Remove Cart Item AJAX
function removeCartItem(itemId) {
    fetch('/cart/remove/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCsrfToken()
        },
        body: `item_id=${itemId}`
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'success') {
            const itemRow = document.querySelector(`.cart-item-row[data-item-id="${itemId}"]`);
            if (itemRow) {
                itemRow.style.opacity = '0';
                itemRow.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    itemRow.remove();
                    if (document.querySelectorAll('.cart-item-row').length === 0) {
                        window.location.reload();
                    }
                }, 300);
            }

            updateCartSummary(data);
            if (data.cart_count !== undefined) {
                updateBadge('#cartBadge, .cart-count', data.cart_count);
            }
            showToast('Item removed from cart', 'info');
        } else {
            showToast(data.message || 'Failed to remove item', 'error');
        }
    })
    .catch(err => {
        showToast('Error removing item', 'error');
    });
}

// Coupon Form Handling
function initCouponForm() {
    const couponForm = document.querySelector('#coupon-form');
    if (!couponForm) return;

    couponForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const codeInput = couponForm.querySelector('input[name="coupon_code"]');
        const code = codeInput ? codeInput.value.trim() : '';

        if (!code) {
            showToast('Please enter a coupon code', 'info');
            return;
        }

        fetch('/cart/apply-coupon/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCsrfToken()
            },
            body: `coupon_code=${encodeURIComponent(code)}`
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'success') {
                showToast(data.message || 'Coupon applied successfully!', 'success');
                setTimeout(() => window.location.reload(), 800);
            } else {
                showToast(data.message || 'Invalid coupon code', 'error');
            }
        })
        .catch(err => {
            showToast('Error applying coupon', 'error');
        });
    });
}

// Helper to update summary elements
function updateCartSummary(data) {
    if (data.subtotal !== undefined) {
        const subtotalElem = document.querySelector('#cart-subtotal');
        if (subtotalElem) subtotalElem.textContent = `₹${data.subtotal}`;
    }
    if (data.discount !== undefined) {
        const discountElem = document.querySelector('#cart-discount');
        if (discountElem) discountElem.textContent = `-₹${data.discount}`;
    }
    if (data.tax !== undefined) {
        const taxElem = document.querySelector('#cart-tax');
        if (taxElem) taxElem.textContent = `₹${data.tax}`;
    }
    if (data.grand_total !== undefined) {
        const grandTotalElem = document.querySelector('#cart-grand-total');
        if (grandTotalElem) grandTotalElem.textContent = `₹${data.grand_total}`;
    }
}
