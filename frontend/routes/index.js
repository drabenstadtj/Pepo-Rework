const express = require('express');
const requireLogin = require('../middleware/requireLogin');
const axios = require('axios');
const isAdmin = require('../middleware/isAdmin');
const attachToken = require('../middleware/attachToken');

const router = express.Router();

const getBackendUrl = (endpoint) => `http://pepo_backend:5000${endpoint}`;

router.get('/', async (req, res) => {
  try {
    // Make the request to your backend to fetch news articles
    const response = await axios.get(getBackendUrl('/news'));
    const newsArticles = response.data;

    // Render the template with the news data
    res.render('index', { user: req.session.user || {}, news: newsArticles });
  } catch (error) {
    console.error('Error fetching news:', error);
    res.render('index', { user: req.session.user || {}, news: [] }); // Pass empty news in case of error
  }
});



router.get('/about', requireLogin, attachToken, (req, res) => {
  res.render('about', { user: req.session.user });
});

module.exports = router;
