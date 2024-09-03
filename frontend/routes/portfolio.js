const express = require('express');
const requireLogin = require('../middleware/requireLogin');
const attachToken = require('../middleware/attachToken');
const config = require('../config/config');
const axios = require('axios');

const router = express.Router();

const getBackendUrl = (endpoint) => `http://localhost:${config.backendPort}${endpoint}`;

router.get('/balance', requireLogin, attachToken, async (req, res) => {
  try {
    const token = req.session.token;
    const response = await axios.get(getBackendUrl('/portfolio/balance'), {
      headers: { 'Authorization': `Bearer ${token}` }
    });

    res.json(response.data);
  } catch (error) {
    console.error('Balance fetch error:', error);
    res.status(500).send("Internal Server Error");
  }
});

router.get('/assets_value', requireLogin, attachToken, async (req, res) => {
  try {
    const token = req.session.token;
    const response = await axios.get(getBackendUrl('/portfolio/assets_value'), {
      headers: { 'Authorization': `Bearer ${token}` }
    });

    res.json(response.data);
  } catch (error) {
    console.error('Assets value fetch error:', error);
    res.status(500).send("Internal Server Error");
  }
});

router.get('/stocks', requireLogin, attachToken, async (req, res) => {
  try {
    const token = req.session.token;
    const response = await axios.get(getBackendUrl('/portfolio/stocks'), {
      headers: { 'Authorization': `Bearer ${token}` }
    });

    res.json(response.data);
  } catch (error) {
    console.error('Portfolio stocks fetch error:', error);
    res.status(500).send("Internal Server Error");
  }
});

module.exports = router;
