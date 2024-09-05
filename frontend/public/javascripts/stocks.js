document.addEventListener("DOMContentLoaded", () => {
  const apiUrl = window.apiUrl;  // Use the global apiUrl variable

  const stocksBody = document.getElementById('stocks-body');
  const symbolHeader = document.getElementById('symbol-header');
  const priceHeader = document.getElementById('price-header');
  const changeHeader = document.getElementById('change-header');

  let stocks = [];
  let sortColumn = 'symbol';
  let sortOrder = 'asc';

  // Function to format the date
  function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    const date = new Date(dateString);
    return date.toLocaleDateString(undefined, options);
  }

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

  fetchStocks();
  setInterval(fetchStocks, 10000); // Update every 10 seconds
});
