document.addEventListener("DOMContentLoaded", () => {
  const apiUrl = window.apiUrl;  // Use the global apiUrl variable
  
  const leaderboardBody = document.getElementById('leaderboard-body');

  async function fetchLeaderboard() {
    try {
      const response = await fetch(`${apiUrl}/leaderboard`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include'
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const users = await response.json();
      updateLeaderboard(users);
    } catch (error) {
      console.error('Error fetching leaderboard data:', error);
    }
  }

  function updateLeaderboard(users) {
    console.log('Updating leaderboard table...');  // Debug: Log when updating
    leaderboardBody.innerHTML = '';  // Clear existing content
    users.forEach((user, index) => {
      const row = document.createElement('tr');

      const rankCell = document.createElement('td');
      rankCell.textContent = index + 1;
      row.appendChild(rankCell);

      const nameCell = document.createElement('td');
      nameCell.textContent = user.username;
      row.appendChild(nameCell);

      const titleCell = document.createElement('td');
      titleCell.textContent = user.title;
      row.appendChild(titleCell);

      const liquidAssetsCell = document.createElement('td');
      liquidAssetsCell.textContent = formatMoney(user.liquidAssets);
      row.appendChild(liquidAssetsCell);

      const investedAssetsCell = document.createElement('td');
      investedAssetsCell.textContent = formatMoney(user.investedAssets);
      row.appendChild(investedAssetsCell);

      const netWorthCell = document.createElement('td');
      netWorthCell.textContent = formatMoney(user.netWorth);
      row.appendChild(netWorthCell);

      leaderboardBody.appendChild(row);
    });
  }

  function formatMoney(value) {
    return `$${value.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ",")}`;
  }

  fetchLeaderboard();
  setInterval(fetchLeaderboard, 10000); // Update every 10 seconds
});
