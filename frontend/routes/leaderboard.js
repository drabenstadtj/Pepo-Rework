const express = require('express');
const requireLogin = require('../middleware/requireLogin');
const attachToken = require('../middleware/attachToken');

const router = express.Router();

router.get('/', requireLogin, attachToken, (req, res) => {
  res.render('leaderboard', { title: 'Leaderboard', user: req.session.user });
});

module.exports = router;
