const express = require('express');
const requireLogin = require('../middleware/requireLogin');
const attachToken = require('../middleware/attachToken');

const router = express.Router();

router.get('/', requireLogin, attachToken, (req, res) => {
  res.render('index', { user: req.session.user });
});

router.get('/about', requireLogin, attachToken, (req, res) => {
  res.render('about', { user: req.session.user });
});

module.exports = router;
