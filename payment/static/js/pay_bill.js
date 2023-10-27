
var stripe = Stripe('{{ stripe_publishable_key }}');
var checkoutButton = document.getElementById('payment_button');
var amountInput = document.getElementById('id_amount');

    checkoutButton.addEventListener('click', function () {
        // Create a new Checkout Session using the server-side endpoint you
        // created in step 3.
        amount = amountInput.value;
        
        fetch("{% url 'api_checkout_session'   %}", {
            method: 'POST',
            body: JSON.stringify(
                { amount : amount }
            )
        })
            .then(function (response) {
                return response.json();
            })
            .then(function (session) {
                return stripe.redirectToCheckout({ sessionId: session.sessionId });
            })
            .then(function (result) {
                // If `redirectToCheckout` fails due to a browser or network
                // error, you should display the localized error message to your
                // customer using `error.message`.
                if (result.error) {
                    alert(result.error.message);
                }
            })
            .catch(function (error) {
                console.error('Error:', error);
            });
    });