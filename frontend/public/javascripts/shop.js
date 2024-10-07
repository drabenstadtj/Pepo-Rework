document.addEventListener('DOMContentLoaded', () => {
  const apiUrl = "https://api.gourdlord.net";  // Use the global apiUrl variable

  const purchaseButtons = document.querySelectorAll('.purchase-button');

  purchaseButtons.forEach(button => {
    button.addEventListener('click', async (event) => {
      const level = event.target.dataset.level;  // This should have the correct 'level' value
      const buttonElement = event.target;

      // Disable button to prevent multiple clicks
      buttonElement.disabled = true;

      try {
        const response = await fetch(`${apiUrl}/shop/purchase`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${document.querySelector('meta[name="csrf-token"]').content}`
          },
          body: JSON.stringify({ level })  // Make sure this is being sent
        });

        const data = await response.json();
        alert(data.message); // Show success or failure message

        if (response.ok) {
          // Force the page to reload after a successful purchase
          window.location.reload();
        }
      } catch (error) {
        console.error('Error purchasing title:', error);
        alert('Error purchasing title.');
      } finally {
        // Re-enable the button after the request completes
        buttonElement.disabled = false;
      }
    });
  });
});
