//'use strict';


var stripe = Stripe('pk_test_51KjPSyIu1jKvkROgukXGhCbkwqwJ28ZDBOJk7iaEuybPsvPQ3cAy6yPrErgcqmcDMYCK15VvqU3h9JQY8IN3ZIlX00wnZzuAcB');

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


var card = elements.create("card", { style: style });
card.mount("#card-element");

card.on('change', function(event) {
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

form.addEventListener('submit', function(ev) {
ev.preventDefault();

var name = document.getElementById("name").value;
var address = document.getElementById("address").value;
var address2 = document.getElementById("address2").value;
var zipcode = document.getElementById("zipcode").value;

  // $.ajax({
  //   type: "POST",
  //   url: 'http://localhost:8000/orders/add/',
  //   data: {
  //     order_key: clientsecret,
  //     csrfmiddlewaretoken: CSRF_TOKEN,
  //     action: "post",
  //   },
  //   success: function (json) {
  //     console.log(json.success)

      stripe.confirmCardPayment(clientsecret, {
        payment_method: {
          card: card,
          billing_details: {
            address:{
                line1:address,
                line2:address2
            },
            name: name
          },
        }
      }).then(function(result) {
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

    // };
    // error: function (xhr, errmsg, err) {},
  // });



});