const jwt = require('jsonwebtoken');
const config = require('../config/config');

const requireLogin = (req, res, next) => {
  if (req.session && req.session.token) {
    try {
      const decoded = jwt.verify(req.session.token, config.secretKey);
      req.user = decoded;
      
      // Add isAdmin flag to the user object (assuming JWT payload contains the role or admin status)
      req.user.isAdmin = decoded.isAdmin || false;

      next();  // User is logged in and JWT is valid, proceed
    } catch (err) {
      console.error('Token verification error:', err);
      res.redirect('/auth/signin');
    }
  } else {
    res.redirect('/auth/signin');  // No session or token, redirect to login
  }
};

module.exports = requireLogin;
