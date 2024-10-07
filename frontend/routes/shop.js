const express = require('express');
const requireLogin = require('../middleware/requireLogin');
const attachToken = require('../middleware/attachToken');
const axios = require('axios');

const router = express.Router();

const getBackendUrl = (endpoint) => `http://pepo_backend:5000${endpoint}`;

router.get('/', requireLogin, attachToken, async (req, res) => {
  try {
    const token = req.session.token;

    // Fetch titles and their prices from the shop endpoint
    const shopResponse = await axios.get(getBackendUrl('/shop/titles'), {
      headers: { 'Authorization': `Bearer ${token}` }
    });

    // Fetch user's balance
    const balanceResponse = await axios.get(getBackendUrl('/portfolio/balance'), {
      headers: { 'Authorization': `Bearer ${token}` }
    });

        // Fetch user's current title
    const titleResponse = await axios.get(getBackendUrl('/portfolio/title'), {
      headers: { 'Authorization': `Bearer ${token}` }
    });

    // Extract title name and level from response
    const { title_level, name: title } = titleResponse.data; // Extract both title_level and name

    const shopData = shopResponse.data; // Array of titles
    const  balance  = balanceResponse.data; // Extract balance

    const formattedBalance = balance.toLocaleString('en-US', {
      style: 'currency',
      currency: 'USD',
    });

    res.render('shop', { 
      user: req.session.user, 
      shopData, 
      token, 
      balance, 
      title_level, 
      title // Include title (name)
    });
    
  } catch (error) {
    console.error('Shop fetch error:', error);
    res.status(500).send("Internal Server Error");
  }
});


module.exports = router;
