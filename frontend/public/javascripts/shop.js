document.addEventListener('DOMContentLoaded', () => {
    const apiUrl = window.apiUrl;  // Use the global apiUrl variable

    const purchaseButtons = document.querySelectorAll('.purchase-button');
  
    purchaseButtons.forEach(button => {
      button.addEventListener('click', async (event) => {
        const level = event.target.dataset.level;
  
        try {
          const response = await fetch(`${apiUrl}/shop/purchase`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${document.querySelector('meta[name="csrf-token"]').content}`
            },
            body: JSON.stringify({ level })
          });
  
          const data = await response.json();
          alert(data.message); // Show success or failure message
          if (response.ok) {
            // Optionally, refresh or update UI
          }
        } catch (error) {
          console.error('Error purchasing title:', error);
          alert('Error purchasing title.');
        }
      });
    });
  });
  