document.addEventListener('DOMContentLoaded', function() {
    const paymentForm = document.querySelector('.payment-form');
    const formFields = document.querySelectorAll('.payment-form-control');

    function validateForm() {
        let isValid = true;
        formFields.forEach(field => {
            if (field.value.trim() === "") {
                isValid = false;
                field.classList.add('border-red-500');
                const label = field.nextElementSibling;
                if (label) {
                    label.classList.add('text-red-500');
                }
            }
        });
        return isValid;
    }

    paymentForm.addEventListener('submit', function(event) {
        event.preventDefault();

        if (validateForm()) {
            const formData = {
                email: document.getElementById('email').value,
                card_number: document.getElementById('card-number').value,
                expiry_date: document.getElementById('expiry-date').value,
                cvv: document.getElementById('cvv').value,
                payment_method: document.querySelector('input[name="payment-method"]:checked').id
            };

            // Send payment data to server
            fetch('/process_payment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Payment processed successfully!');
                    paymentForm.reset();
                } else {
                    alert(data.message || 'Payment processing failed.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while processing the payment.');
            });
        } else {
            alert('Please fill in all required fields.');
        }
    });
});