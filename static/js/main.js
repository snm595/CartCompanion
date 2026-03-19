/**
 * main.js — Shared add-to-cart functionality
 * Used by all category pages (clothes, mobiles, furniture, appliances)
 */
document.addEventListener('DOMContentLoaded', () => {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];

    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', () => {
            const product = {
                name: button.getAttribute('data-name'),
                price: button.getAttribute('data-price'),
                image: button.getAttribute('data-image'),
                quantity: 1
            };

            cart.push(product);
            localStorage.setItem('cart', JSON.stringify(cart));

            // Update cart badge
            const badge = document.getElementById('cart-count');
            if (badge) badge.textContent = cart.length;

            alert(`${product.name} has been added to the cart!`);
            window.location.href = "/cart";
        });
    });
});
