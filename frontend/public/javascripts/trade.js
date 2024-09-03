document.addEventListener("DOMContentLoaded", function() {
  const apiUrl = window.apiUrl;  // Use the global apiUrl variable

  const token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
  const stockSymbolInput = document.getElementById('stockSymbol');
  const stockPriceInput = document.getElementById('stockPrice');
  const numberOfSharesInput = document.getElementById('numberOfShares');
  const totalPriceInput = document.getElementById('totalPrice');

  if (!token) {
    alert('User is not authenticated');
    window.location.href = '/signin';  // Redirect to sign-in page if not authenticated
    return;
  }

  const balance = document.querySelector('meta[name="balance"]').getAttribute('content');
  document.getElementById('balance').textContent = numberWithCommas(parseFloat(balance).toFixed(2));
  const investment = document.querySelector('meta[name="assets_value"]').getAttribute('content');
  document.getElementById('investment').textContent = numberWithCommas(parseFloat(investment).toFixed(2));

  document.getElementById('stockSymbol').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {  // Enter key pressed
      e.preventDefault();
      document.getElementById('getPriceButton').click();  // Trigger get price function
    }
  });

  document.getElementById('getPriceButton').addEventListener('click', function() {
    const symbol = document.getElementById('stockSymbol').value;
    if (symbol) {
      fetch(`${apiUrl}/stocks/${symbol}`, {
        method: 'GET',
        headers: { 'Authorization': `Bearer ${token}` },
        credentials: 'include'
      })
      .then(response => response.json())
      .then(data => {
        if (data.price) {
          const roundedPrice = parseFloat(data.price).toFixed(2);
          document.getElementById('stockPrice').value = roundedPrice;
          calculateTotalPrice();
        } else {
          alert('Stock not found');
        }
      })
      .catch(() => {
        alert('Error fetching stock price');
      });
    } else {
      alert('Please enter a stock symbol');
    }
  });

  document.getElementById('numberOfShares').addEventListener('input', function() {
    calculateTotalPrice();
  });

  function calculateTotalPrice() {
    const price = parseFloat(document.getElementById('stockPrice').value);
    const shares = parseInt(document.getElementById('numberOfShares').value);
    if (!isNaN(price) && !isNaN(shares) && shares > 0) {
      const totalPrice = (price * shares).toFixed(2);
      document.getElementById('totalPrice').value = totalPrice;
    } else {
      document.getElementById('totalPrice').value = '';
    }
  }

  document.getElementById('buyButton').addEventListener('click', function(e) {
    e.preventDefault();
    submitTransaction('buy');
  });

  document.getElementById('sellButton').addEventListener('click', function(e) {
    e.preventDefault();
    submitTransaction('sell');
  });

  function submitTransaction(type) {
    const stockSymbol = document.getElementById('stockSymbol').value;
    const quantity = parseInt(document.getElementById('numberOfShares').value);

    if (!stockSymbol || isNaN(quantity) || quantity <= 0) {
      alert('Please fill in all fields with valid values');
      return;
    }

    fetch(`${apiUrl}/transactions/${type}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        stock_symbol: stockSymbol,
        quantity: quantity
      })
    })
    .then(response => response.json())
    .then(response => {
      alert(response.message || 'Transaction successful');
      clearFields();  // Clear fields after successful transaction
      location.reload();  // Refresh the page on successful transaction
    })
    .catch(error => {
      alert('Transaction failed');
      clearFields();  // Clear fields even if the transaction fails
    });
  }

  function clearFields() {
    document.getElementById('stockSymbol').value = '';
    document.getElementById('stockPrice').value = '';
    document.getElementById('numberOfShares').value = '';
    document.getElementById('totalPrice').value = '';
  }

  function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }

  function clearOtherInputs() {
    stockPriceInput.value = '';
    numberOfSharesInput.value = '';
    totalPriceInput.value = '';
  }

  // Add event listener to validate numberOfShares input
  numberOfSharesInput.addEventListener('input', () => {
    numberOfSharesInput.value = numberOfSharesInput.value.split('.')[0];
  });

  // Add event listener to the stockSymbol input
  stockSymbolInput.addEventListener('input', clearOtherInputs);

  document.querySelectorAll('.portfolio-table tbody tr').forEach(row => {
    row.addEventListener('click', function() {
      const stockSymbol = this.cells[0].textContent.trim();
      stockSymbolInput.value = stockSymbol;
      clearOtherInputs();
    });
  });
});
