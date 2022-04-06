//'use strict';


var stripe = Stripe(STRIPE_PUBLIC_KEY);

var elem = document.getElementById('submit');
clientsecret = elem.getAttribute('data-secret');

// Set up Stripe.js and Elements to use in checkout form
var elements = stripe.elements();
var style = {
	base: {
		color: "#000",
		lineHeight: '2.4',
		fontSize: '16px'
	}
};


var card = elements.create("card", {style: style});
card.mount("#card-element");

card.on('change', function (event) {
	var displayError = document.getElementById('card-errors')
	if (event.error) {
		displayError.textContent = event.error.message;
		$('#card-errors').addClass('alert alert-info');
	} else {
		displayError.textContent = '';
		$('#card-errors').removeClass('alert alert-info');
	}
});

var form = document.getElementById('payment-form');

form.addEventListener('submit', function (ev) {
	ev.preventDefault();

	var name = document.getElementById("name").value;
	var email = document.getElementById("email").value;
	var phone = document.getElementById("phone").value;
	var address = document.getElementById("address").value;
	var address2 = document.getElementById("address2").value;
	var city = document.getElementById("city").value;
	var country = document.getElementById("country").value;
	var state = document.getElementById("state").value;
	var zipcode = document.getElementById("zipcode").value;

	$.ajax({
		type: "POST",
		url: 'http://localhost:8000/order/add/',
		data: {
			order_key: clientsecret,
			csrfmiddlewaretoken: CSRF_TOKEN,
			action: "post",
			name: name,
			phone: phone,
			address: address,
			address2: address2,
			city: city,
			country: country,
			state: state,
			zipcode: zipcode
		},
		success: function (json) {
			console.log(json.success)

			stripe.confirmCardPayment(clientsecret, {
				payment_method: {
					card: card,
					billing_details: {
						address: {
							city: city,
							country: country,
							line1: address,
							line2: address2,
							postal_code: zipcode,
							state: state
						},
						email: email,
						name: name
					},
				}
			}).then(function (result) {
				if (result.error) {
					console.log('payment error')
					console.log(result.error.message);
				} else {
					if (result.paymentIntent.status === 'succeeded') {
						console.log('payment processed')
						// There's a risk of the customer closing the window before callback
						// execution. Set up a webhook or plugin to listen for the
						// payment_intent.succeeded event that handles any business critical
						// post-payment actions.
						window.location.replace("http://localhost:8000/payment/orderplaced/");
					}
				}
			});
		},
		error: function (xhr, errmsg, err) {
		},
	});
});