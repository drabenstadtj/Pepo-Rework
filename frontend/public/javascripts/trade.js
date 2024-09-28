document.addEventListener("DOMContentLoaded", function () {
  const apiUrl = window.apiUrl;  // Use the global apiUrl variable
  const token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
  const stockSymbolInput = document.getElementById('stockSymbol');
  const stockPriceInput = document.getElementById('stockPrice');
  const numberOfSharesInput = document.getElementById('numberOfShares');
  const totalPriceInput = document.getElementById('totalPrice');
  const dropdownContent = document.getElementById('dropdown-content');
  const balanceElement = document.getElementById('balance');
  const investmentElement = document.getElementById('investment');
  
  // Fetch the initial values for balance and invested assets
  const balance = parseFloat(document.querySelector('meta[name="balance"]').getAttribute('content'));
  const investment = parseFloat(document.querySelector('meta[name="assets_value"]').getAttribute('content'));

  // Set initial values on the page
  updateBalanceAndInvestment(balance, investment);

  // Function to update balance and investment elements
  function updateBalanceAndInvestment(balance, investment) {
    balanceElement.textContent = numberWithCommas(balance.toFixed(2));
    investmentElement.textContent = numberWithCommas(investment.toFixed(2));
  }

  // Function to filter the dropdown based on input
  window.filterStocks = function () {
    const query = stockSymbolInput.value.toLowerCase();
    dropdownContent.innerHTML = '';  // Clear previous content

    if (query.length > 0) {
      // Filter stocks based on the query
      const filteredStocks = allStocks.filter(stock => stock.symbol.toLowerCase().includes(query));

      // Populate the dropdown with matching stocks
      filteredStocks.forEach(stock => {
        const a = document.createElement('a');
        a.href = 'javascript:void(0)';
        a.textContent = stock.symbol;
        a.addEventListener('click', function () {
          stockSymbolInput.value = stock.symbol;
          dropdownContent.classList.remove('show');  // Hide dropdown when a stock is clicked
          fetchStockPrice(stock.symbol);  // Fetch the stock price for the selected symbol
        });
        dropdownContent.appendChild(a);
      });

      // Show the dropdown if there are matches
      if (filteredStocks.length > 0) {
        dropdownContent.classList.add('show');
      } else {
        dropdownContent.classList.remove('show');
      }
    } else {
      dropdownContent.classList.remove('show');
    }
  };

  // Fetch stock price based on the symbol entered or selected
  function fetchStockPrice(symbol) {
    fetch(`${apiUrl}/stocks/${symbol}`, {
      method: 'GET',
      headers: { 'Authorization': `Bearer ${token}` },
      credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
      if (data.price) {
        stockPriceInput.value = parseFloat(data.price).toFixed(2);  // Populate the stock price
        calculateTotalPrice();  // Calculate total price when stock price is fetched
      } else {
        alert('Stock not found');
        stockPriceInput.value = '';  // Clear the stock price if not found
        totalPriceInput.value = '';  // Clear the total price if stock is not found
      }
    })
    .catch(() => {
      alert('Error fetching stock price');
      stockPriceInput.value = '';  // Clear the stock price on error
      totalPriceInput.value = '';  // Clear the total price on error
    });
  }

  // Add event listener to fetch stock price when pressing Enter in the input
  stockSymbolInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
      e.preventDefault();
      const symbol = stockSymbolInput.value.trim();
      if (symbol) {
        fetchStockPrice(symbol);  // Fetch the stock price when pressing Enter
      }
    }
  });

  // Add event listener to calculate total price when number of shares is entered
  numberOfSharesInput.addEventListener('input', function () {
    calculateTotalPrice();  // Calculate total price whenever the number of shares is changed
  });

  // Function to calculate total price based on stock price and number of shares
  function calculateTotalPrice() {
    const price = parseFloat(stockPriceInput.value);
    const shares = parseInt(numberOfSharesInput.value);
    if (!isNaN(price) && !isNaN(shares) && shares > 0) {
      const totalPrice = (price * shares).toFixed(2);
      totalPriceInput.value = totalPrice;
    } else {
      totalPriceInput.value = '';  // Clear total price if inputs are invalid
    }
  }

  // Function to update balance and investment after a transaction
  function updateAssetsAfterTransaction(newBalance, newInvestment) {
    updateBalanceAndInvestment(newBalance, newInvestment);
  }

  // Hide dropdown when clicked outside of the input
  document.addEventListener('click', function (event) {
    if (!event.target.matches('#stockSymbol')) {
      dropdownContent.classList.remove('show');
    }
  });

  // Transaction functions (Buy/Sell) would go here, and should update the balance and invested assets
  document.getElementById('buyButton').addEventListener('click', function(e) {
    e.preventDefault();
    // Implement buy transaction logic here and update the assets after the transaction
    performTransaction('buy');
  });

  document.getElementById('sellButton').addEventListener('click', function(e) {
    e.preventDefault();
    // Implement sell transaction logic here and update the assets after the transaction
    performTransaction('sell');
  });

  function performTransaction(type) {
    const stockSymbol = stockSymbolInput.value;
    const quantity = parseInt(numberOfSharesInput.value);
    const totalPrice = parseFloat(totalPriceInput.value);
  
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
      body: JSON.stringify({ stock_symbol: stockSymbol, quantity })
    })
    .then(response => {
      // Check if the response is a success (HTTP 200)
      if (!response.ok) {
        return response.json().then(data => { throw new Error(data.error || 'Transaction failed') });
      }
      return response.json();  // Parse the JSON response
    })
    .then(data => {
      // Success handling
      alert(data.message);  // Show success message
      clearForm();  // Clear the form fields
      location.reload();  // Reload the page on successful transaction
    })
    .catch(error => {
      // Error handling
      alert(error.message || 'Transaction failed');
    });
  }
  
  // Function to clear the form after a transaction
  function clearForm() {
    stockSymbolInput.value = '';
    stockPriceInput.value = '';
    numberOfSharesInput.value = '';
    totalPriceInput.value = '';
  }
  // Utility to format numbers with commas
  function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }
});
