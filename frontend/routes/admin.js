const express = require('express');
const axios = require('axios');
const isAdmin = require('../middleware/isAdmin');
const router = express.Router();

const getBackendUrl = (endpoint) => `http://pepo_backend:5000${endpoint}`;

router.get('/', isAdmin, async (req, res) => {
    try {
        // Fetch all stocks
        const response = await axios.get(getBackendUrl('/stocks/list'));

        // Render the admin page with the stock list
        res.render('admin', { user: req.session.user, stocks: response.data });
    } catch (error) {
        console.error('Error fetching stock list:', error);
        req.flash('error', 'Unable to fetch stock data');
        res.redirect('/');
    }
});

router.post('/stocks/:symbol/update_volatility', isAdmin, async (req, res) => {
    try {
        const { symbol } = req.params;  // Ensure symbol is correctly destructured here
        const { volatility_factor } = req.body;

        const response = await axios.post(
            getBackendUrl(`/admin/stocks/${symbol}/update_volatility`),
            { volatility_factor: parseFloat(volatility_factor) }
        );

        res.redirect('/admin');
    } catch (error) {
        console.error(`Error updating stock volatility for ${req.params.symbol}:`, error);  // Ensure symbol is passed
        res.redirect('/admin');
    }
});


router.post('/stocks/:symbol/update_trend', isAdmin, async (req, res) => {
    try {
        const { symbol } = req.params;
        const { trend_direction } = req.body;

        const response = await axios.post(
            getBackendUrl(`/admin/stocks/${symbol}/update_trend`),
            { trend_direction: parseFloat(trend_direction) }
        );


        res.redirect('/admin');
    } catch (error) {
        console.error(`Error updating stock trend direction for ${symbol}:`, error);
        res.redirect('/admin');
    }
});

  
module.exports = router;
// Render the admin dashboard
router.get('/', isAdmin, (req, res) => {
  res.render('admin', { user: req.session.user });
});

// Handle the tester entry insertion
router.post('/add-tester', isAdmin, async (req, res) => {
  try {
    // Define the tester entry
    const testerEntry = {
      title: "Breaking News: Tech Stocks Soar",
      content: "Tech stocks surged today, with major gains in the software sector. Analysts attribute the rise to recent earnings reports that exceeded expectations.",
      author: "Jane Doe",
      timestamp: new Date(),
      isFeatured: true,
      thumbnail: "https://example.com/image.jpg"
    };

    // Send a POST request to the backend to insert the entry
    await axios.post(getBackendUrl('/news'), testerEntry);

    // Redirect back to the admin dashboard with a success message
    res.redirect('/admin?success=Tester entry added');
  } catch (error) {
    console.error("Error adding tester entry:", error);
    res.redirect('/admin?error=Failed to add tester entry');
  }
});

module.exports = router;
