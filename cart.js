function updateCartCount() {
    var cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];
    var cartItemCount = document.getElementById('cartItemCount');
    if (cartItemCount) {
        cartItemCount.innerText = cartItems.length;
    }
}

// Call updateCartCount when the DOM content is loaded
document.addEventListener('DOMContentLoaded', function () {
    updateCartCount();
});
