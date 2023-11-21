
const paymentForm = document.getElementById('pay');
paymentForm.addEventListener("submit", payWithPaystack, false);
function payWithPaystack(e) {
    e.preventDefault();
    let handler = PaystackPop.setup({
        
        key: '{{paystack_public_key}}', // Replace with your public key
        email: '{{ user.email }}',
        amount: '{{ total }}' * 100,
        ref: '{{ref}}', // generates a pseudo-unique reference. Please replace with a reference you generated. Or remove the line entirely so our API will generate one for you
        // label: "Optional string that replaces customer email"
        onClose: function () {
            alert('Window closed.');
        },
        callback: function(response) {
            window.location = "http://localhost:8000/verify_transaction.php?reference=" + response.reference;
          }
    });
    handler.openIframe();
}