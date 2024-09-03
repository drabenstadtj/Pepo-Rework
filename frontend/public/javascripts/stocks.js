document.addEventListener("DOMContentLoaded", () => {
  const apiUrl = 'http://localhost:5000'  // Use the global apiUrl variable
  const socket = io('http://localhost:5000'); // Adjust this to match your frontend server's URL

  const stocksBody = document.getElementById('stocks-body');
  const symbolHeader = document.getElementById('symbol-header');
  const priceHeader = document.getElementById('price-header');
  const changeHeader = document.getElementById('change-header');

  let stocks = [];
  let sortColumn = 'symbol';
  let sortOrder = 'asc';

  socket.on('connect', () => {
    console.log('Connected to WebSocket server');
  });

  socket.on('disconnect', () => {
    console.log('Disconnected from WebSocket server');
  });

  socket.on('stock_update', (updatedStock) => {
    // Update the stock in the local stocks array
    const index = stocks.findIndex(stock => stock.symbol === updatedStock.symbol);
    if (index !== -1) {
      stocks[index] = updatedStock;
    } else {
      stocks.push(updatedStock);
    }
    sortAndUpdateStocks();
  });

  async function fetchStocks() {
    try {
      const response = await fetch(`${apiUrl}/stocks/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include'
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

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
      
      if (valueA < valueB) return sortOrder === 'asc' ? -1 : 1;
      if (valueA > valueB) return sortOrder === 'asc' ? 1 : -1;
      return 0;
    });
    updateStocks(stocks);
    updateHeaderArrows();
  }

  function updateHeaderArrows() {
    // Reset headers
    symbolHeader.textContent = 'Symbol';
    priceHeader.textContent = 'Price';
    changeHeader.textContent = 'Change';

    // Add arrows
    const arrow = sortOrder === 'asc' ? '↑' : '↓';
    if (sortColumn === 'symbol') {
      symbolHeader.textContent += ` ${arrow}`;
    } else if (sortColumn === 'price') {
      priceHeader.textContent += ` ${arrow}`;
    } else if (sortColumn === 'change') {
      changeHeader.textContent += ` ${arrow}`;
    }
  }

  function updateStocks(stocks) {
    console.log('Updating stocks table...');  // Debug: Log when updating
    stocksBody.innerHTML = '';  // Clear existing content
    stocks.forEach(stock => {
      const row = document.createElement('tr');

      const symbolCell = document.createElement('td');
      symbolCell.classList.add('stock-popup');
      const symbolSpan = document.createElement('span');
      symbolSpan.textContent = stock.symbol;
      const popupDiv = document.createElement('div');
      popupDiv.classList.add('popuptext');
      popupDiv.innerHTML = `
        <h3>${stock.symbol}</h3>
        <p>Name: ${stock.name}</p>
        <p>Sector: ${stock.sector}</p>
        <p>Low: $${stock.low.toFixed(2)}</p>
        <p>High: $${stock.high.toFixed(2)}</p>
        <p>Updated: ${formatDate(stock.last_update)}</p>
      `;
      symbolCell.appendChild(symbolSpan);
      symbolCell.appendChild(popupDiv);
      row.appendChild(symbolCell);

      const priceCell = document.createElement('td');
      priceCell.textContent = "$" + stock.price.toFixed(2);
      row.appendChild(priceCell);

      const changeCell = document.createElement('td');
      changeCell.textContent = stock.change.toFixed(2);
      changeCell.classList.add(stock.change >= 0 ? 'positive-change' : 'negative-change');
      row.appendChild(changeCell);

      stocksBody.appendChild(row);
    });
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

  fetchStocks();  // Initial fetch to populate the table
  // Remove the setInterval call as we are now using WebSocket for real-time updates
});
