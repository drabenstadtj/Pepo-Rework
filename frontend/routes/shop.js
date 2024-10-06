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

    const shopData = shopResponse.data; // This should be an array of titles
    console.log(shopData)

    res.render('shop', { user: req.session.user, shopData, token });
  } catch (error) {
    console.error('Shop fetch error:', error);
    res.status(500).send("Internal Server Error");
  }
});

module.exports = router;
