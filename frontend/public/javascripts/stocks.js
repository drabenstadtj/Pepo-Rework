document.addEventListener("DOMContentLoaded", () => {
  const apiUrl = window.apiUrl;

  const stocksBody = document.getElementById('stocks-body');
  const symbolHeader = document.getElementById('symbol-header');
  const priceHeader = document.getElementById('price-header');
  const changeHeader = document.getElementById('change-header');

  let stocks = [];
  let sortColumn = 'symbol';
  let sortOrder = 'asc';

  function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    const date = new Date(dateString);
    return date.toLocaleDateString(undefined, options);
  }

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
      changeCell.classList.add(stock.change >= 0 ? 'positive-change' : 'negative-change');
      row.appendChild(changeCell);

      // Add click event to the row to toggle the additional details
      row.addEventListener('click', () => toggleStockDetails(row, stock));

      stocksBody.appendChild(row);
    });
  }

  function toggleStockDetails(row, stock) {
    // Check if the details row already exists (i.e., if the row is already expanded)
    const nextRow = row.nextElementSibling;
    if (nextRow && nextRow.classList.contains('details-row')) {
      nextRow.remove(); // If details row exists, remove it (toggle off)
    } else {
      // Create a new row for the expanded details
      const detailsRow = document.createElement('tr');
      detailsRow.classList.add('details-row');

      const detailsCell = document.createElement('td');
      detailsCell.colSpan = 3; // Span across all table columns
      detailsCell.innerHTML = `
        <div>
          <strong>Name:</strong> ${stock.name}<br>
          <strong>Sector:</strong> ${stock.sector}<br>
          <strong>Low:</strong> $${stock.low.toFixed(2)}<br>
          <strong>High:</strong> $${stock.high.toFixed(2)}<br>
          <strong>Last Updated:</strong> ${formatDate(stock.last_update)}
        </div>
      `;
      detailsRow.appendChild(detailsCell);

      // Insert the details row just after the clicked row
      row.parentNode.insertBefore(detailsRow, row.nextSibling);
    }
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
