const express = require('express');
const requireLogin = require('../middleware/requireLogin');
const attachToken = require('../middleware/attachToken');
const config = require('../config/config');
const axios = require('axios');

const router = express.Router();

const getBackendUrl = (endpoint) => `http://pepo_backend:5000${endpoint}`;

router.get('/', requireLogin, attachToken, async (req, res) => {
  try {
    const response = await axios.get(getBackendUrl('/stocks'));
    const stocks = response.data;
    const token = req.session.token;

    res.render('stocks', { stocks, user: req.session.user, token });
  } catch (error) {
    console.error('Stocks fetch error:', error);
    res.status(500).send("Internal Server Error");
  }
});

module.exports = router;
