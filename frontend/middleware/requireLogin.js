const jwt = require('jsonwebtoken');
const config = require('../config/config');

const requireLogin = (req, res, next) => {
  if (req.session && req.session.token) {
    try {
      const decoded = jwt.verify(req.session.token, config.secretKey);
      req.user = decoded;
      next();
    } catch (err) {
      console.error('Token verification error:', err);
      res.redirect('/auth/signin');
    }
  } else {
    res.redirect('/auth/signin');
  }
};

module.exports = requireLogin;
