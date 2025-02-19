// static/script.js

document.addEventListener('DOMContentLoaded', () => {
    const paymentForm = document.getElementById('paymentForm');
    const transactionsList = document.getElementById('transactionsList');

    paymentForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const upiId = document.getElementById('upiId').value;
        const amount = document.getElementById('amount').value;
        const description = document.getElementById('description').value;

        try {
            const response = await fetch('/make_payment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ upi_id: upiId, amount: amount, description: description })
            });

            const data = await response.json();

            if (response.ok) {
                alert('Payment successful!');
                paymentForm.reset();
                await loadTransactions(); // Reload transactions after successful payment
            } else {
                alert(data.error || 'Payment failed.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred.');
        }
    });

    async function loadTransactions() {
        try {
            const response = await fetch('/get_transactions');
            const transactions = await response.json();

            transactionsList.innerHTML = ''; 

            if (transactions.length === 0) {
                transactionsList.innerHTML = "<p>No transactions yet.</p>";
                return;
            }

            const table = document.createElement('table');
            table.innerHTML = `
                <thead>
                    <tr><th>UPI ID</th><th>Amount</th><th>Description</th><th>Timestamp</th></tr>
                </thead>
                <tbody>
                    ${transactions.map(t => `
                        <tr>
                            <td>${t.upi_id}</td>
                            <td>₹${t.amount}</td>
                            <td>${t.description || '-'}</td>
                            <td>${t.timestamp}</td>
                        </tr>`).join('')}
                </tbody>`;

            transactionsList.appendChild(table);
        } catch (error) {
            console.error('Error loading transactions:', error);
            transactionsList.innerHTML = "<p>Error loading transactions.</p>";
        }
    }

    loadTransactions();
});