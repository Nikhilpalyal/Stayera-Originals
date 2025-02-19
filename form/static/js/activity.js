document.querySelector('.modify-button').addEventListener('click', function() {
    let name = prompt("Enter your name:", "Nikhil");
    let email = prompt("Enter your email:", "nikhilpalyal6@gmail.com");
    let phone = prompt("Enter your phone number:", "8264131474");

    if (name && email && phone) {
        fetch('/update_user', {
            method: 'POST',
            body: new URLSearchParams({ name, email, phone }),
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("user-info").innerText = `${name} | ${email} | ${phone}`;
            alert(data.message);
        });
    }
});

document.getElementById('pay-now').addEventListener('click', function() {
    fetch('/payment')
    .then(response => response.json())
    .then(data => {
        document.getElementById('upi-id').innerText = data.upi_id;
        document.getElementById('qr-code').src = data.qr_code;
        document.getElementById('payment-details').style.display = 'block';
    });
});
document.getElementById("payNow").addEventListener("click", function() {
    let dropdown = document.getElementById("paymentDropdown");
    if (dropdown.style.display === "block") {
        dropdown.style.display = "none";
    } else {
        dropdown.style.display = "block";
    }
});
