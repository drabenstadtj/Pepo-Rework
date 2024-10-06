document.addEventListener("DOMContentLoaded", () => {
  const apiUrl = window.apiUrl;
  const stocksBody = document.getElementById('stocks-body');
  const symbolHeader = document.getElementById('symbol-header');
  const priceHeader = document.getElementById('price-header');
  const changeHeader = document.getElementById('change-header');
  const stockInfoCard = document.getElementById('stock-info-card');
  
  let stocks = [];
  let selectedStock = null; // Keep track of the selected stock symbol
  let sortColumn = 'symbol';
  let sortOrder = 'asc';

  async function fetchStocks() {
    try {
      const response = await fetch(`${apiUrl}/stocks/list`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
      });

      if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

      stocks = await response.json();
      sortAndUpdateStocks();
    } catch (error) {
      console.error('Error fetching stocks data:', error);
    }
  }

  function sortAndUpdateStocks() {
    stocks.sort((a, b) => {
      let valueA, valueB;
      if (sortColumn === 'price') {
        valueA = parseFloat(a.price);
        valueB = parseFloat(b.price);
      } else if (sortColumn === 'change') {
        valueA = parseFloat(a.change);
        valueB = parseFloat(b.change);
      } else {
        valueA = a[sortColumn];
        valueB = b[sortColumn];
      }
      return valueA < valueB ? (sortOrder === 'asc' ? -1 : 1) : valueA > valueB ? (sortOrder === 'asc' ? 1 : -1) : 0;
    });
    updateStocks(stocks);
    updateHeaderArrows();
  }

  function updateHeaderArrows() {
    symbolHeader.textContent = 'Symbol';
    priceHeader.textContent = 'Price';
    changeHeader.textContent = 'Change';

    const arrow = sortOrder === 'asc' ? '↑' : '↓';
    if (sortColumn === 'symbol') symbolHeader.textContent += ` ${arrow}`;
    else if (sortColumn === 'price') priceHeader.textContent += ` ${arrow}`;
    else if (sortColumn === 'change') changeHeader.textContent += ` ${arrow}`;
  }

  function updateStocks(stocks) {
    stocksBody.innerHTML = ''; 
    stocks.forEach(stock => {
      const row = document.createElement('tr');
  
      const symbolCell = document.createElement('td');
      symbolCell.classList.add('stock-popup');
      symbolCell.textContent = stock.symbol;
      row.appendChild(symbolCell);
  
      const priceCell = document.createElement('td');
      priceCell.textContent = `$${stock.price.toFixed(2)}`;
      row.appendChild(priceCell);
  
      const changeCell = document.createElement('td');
      changeCell.textContent = stock.change.toFixed(2);
      changeCell.classList.add(stock.change >= 0 ? 'positive' : 'negative');
      row.appendChild(changeCell);
  
      row.addEventListener('click', () => {
        selectedStock = stock.symbol;
        displayStockInfo(stock);
      });
  
      stocksBody.appendChild(row);
    });

    // After the table is updated, if a stock was previously selected, re-display its info
    if (selectedStock) {
      const selected = stocks.find(stock => stock.symbol === selectedStock);
      if (selected) displayStockInfo(selected);
    }
  }

  function displayStockInfo(stock) {

    stockInfoCard.innerHTML = `
      <h3>Stock Details</h3>
      <p><strong>Name:</strong> ${stock.name}</p>
      <p><strong>Symbol:</strong> ${stock.symbol}</p>
      <p><strong>Price:</strong> $${stock.price.toFixed(2)}</p>
      <p><strong>Change:</strong> ${stock.change.toFixed(2)}</p>
      <p><strong>Last Updated:</strong> ${formatDate(stock.last_update)}</p>
    `;
  }

  symbolHeader.addEventListener('click', () => {
    sortColumn = 'symbol';
    sortOrder = sortOrder === 'asc' ? 'desc' : 'asc';
    sortAndUpdateStocks();
  });

  priceHeader.addEventListener('click', () => {
    sortColumn = 'price';
    sortOrder = sortOrder === 'asc' ? 'desc' : 'asc';
    sortAndUpdateStocks();
  });

  changeHeader.addEventListener('click', () => {
    sortColumn = 'change';
    sortOrder = sortOrder === 'asc' ? 'desc' : 'asc';
    sortAndUpdateStocks();
  });

  function formatDate(dateString) {
    // Create a date object from the ISO string
    const date = new Date(dateString);
    
    // Check if the date is valid
    if (isNaN(date.getTime())) {
        console.error("Invalid date string:", dateString);
        return "Invalid Date"; // or return a default string
    }

    // Options for formatting the date
    const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        timeZoneName: 'short' // Optional: include the time zone name
    };

    // Return the formatted date string
    return date.toLocaleString(undefined, options);
}

  

  setInterval(fetchStocks, 10000);
  fetchStocks(); // Initial load
});
