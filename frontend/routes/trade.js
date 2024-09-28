const express = require('express');
const requireLogin = require('../middleware/requireLogin');
const attachToken = require('../middleware/attachToken');
const config = require('../config/config');
const axios = require('axios');

const router = express.Router();

const getBackendUrl = (endpoint) => `http://pepo_backend:5000${endpoint}`;

router.get('/', requireLogin, attachToken, async (req, res) => {
  try {
    const token = req.session.token;
    const portfolioResponse = await axios.get(getBackendUrl('/portfolio/stocks'), {
      headers: { 'Authorization': `Bearer ${token}` }
    });

    const balanceResponse = await axios.get(getBackendUrl('/portfolio/balance'), {
      headers: { 'Authorization': `Bearer ${token}` }
    });

    const assetsValueResponse = await axios.get(getBackendUrl('/portfolio/assets_value'), {
      headers: { 'Authorization': `Bearer ${token}` }
    });

    // Fetch all stock symbols
    const stockSymbolsResponse = await axios.get(getBackendUrl('/stocks/list'), {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    
    const portfolio = portfolioResponse.data;
    const balance = balanceResponse.data;
    const assets_value = assetsValueResponse.data;
    const allStocks = stockSymbolsResponse.data;  // Pass the stock symbols to the template
    
    res.render('trade', { user: req.session.user, portfolio, balance, assets_value, token, allStocks });
  } catch (error) {
    console.error('Trade fetch error:', error);
    res.status(500).send("Internal Server Error");
  }
});


module.exports = router;
