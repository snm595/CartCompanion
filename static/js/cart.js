/**
 * cart.js — Cart page logic
 * Reads cart from localStorage, displays items with quantity controls,
 * handles remove, and shows payment options.
 */
document.addEventListener('DOMContentLoaded', () => {
    const cartItemsContainer = document.getElementById('cart-items');
    const totalAmountContainer = document.getElementById('total-amount');
    const cartSummary = document.getElementById('cart-summary');
    const buyButton = document.getElementById('buy-button');
    const paymentOptionsContainer = document.getElementById('payment-options');
    let cart = JSON.parse(localStorage.getItem('cart')) || [];

    // If cart is empty, show message and hide summary
    if (cart.length === 0) {
        cartItemsContainer.innerHTML = '<p class="cart-empty">Your cart is empty!</p>';
        return;
    }

    // Show summary section
    cartSummary.style.display = 'block';

    let totalAmount = 0;

    // Display cart items
    cart.forEach((item, index) => {
        const cartItem = document.createElement('div');
        cartItem.className = 'cart-item';

        const imageUrl = item.image
            ? `/static/images/${item.image}`
            : '/static/images/LOGO.jpg';

        const qty = (item.quantity && item.quantity > 0) ? item.quantity : 1;

        cartItem.innerHTML = `
            <img src="${imageUrl}" alt="${item.name}">
            <div class="cart-item-info">
                <h3>${item.name}</h3>
                <p class="price">₹${item.price}</p>
            </div>
            <div class="quantity-controls">
                <button class="decrease-quantity" data-index="${index}">−</button>
                <span class="quantity">${qty}</span>
                <button class="increase-quantity" data-index="${index}">+</button>
            </div>
            <button class="remove-item" data-index="${index}">Remove</button>
        `;

        cartItemsContainer.appendChild(cartItem);
        totalAmount += parseFloat(item.price.replace(/,/g, '')) * qty;
    });

    // Update total
    totalAmountContainer.textContent = `Total: ₹${totalAmount.toFixed(2)}`;

    // Remove item
    document.querySelectorAll('.remove-item').forEach(button => {
        button.addEventListener('click', (e) => {
            const index = e.target.getAttribute('data-index');
            cart.splice(index, 1);
            localStorage.setItem('cart', JSON.stringify(cart));
            window.location.reload();
        });
    });

    // Increase quantity
    document.querySelectorAll('.increase-quantity').forEach(button => {
        button.addEventListener('click', (e) => {
            const index = e.target.getAttribute('data-index');
            cart[index].quantity = (cart[index].quantity || 1) + 1;
            saveAndReload();
        });
    });

    // Decrease quantity
    document.querySelectorAll('.decrease-quantity').forEach(button => {
        button.addEventListener('click', (e) => {
            const index = e.target.getAttribute('data-index');
            if ((cart[index].quantity || 1) > 1) {
                cart[index].quantity -= 1;
            }
            saveAndReload();
        });
    });

    function saveAndReload() {
        localStorage.setItem('cart', JSON.stringify(cart));
        window.location.reload();
    }

    // Buy button shows payment options
    buyButton.addEventListener('click', () => {
        paymentOptionsContainer.style.display = 'block';
    });

    // Payment method selection
    document.getElementById('credit-card-option').addEventListener('click', () => {
        alert('You selected Credit/Debit Card. Proceeding to payment.');
    });

    document.getElementById('paypal-option').addEventListener('click', () => {
        alert('You selected PayPal. Proceeding to PayPal.');
    });

    document.getElementById('upi-option').addEventListener('click', () => {
        alert('You selected UPI. Please enter UPI ID.');
    });
});
