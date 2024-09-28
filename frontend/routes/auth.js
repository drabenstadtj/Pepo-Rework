const express = require('express');
const axios = require('axios');
const config = require('../config/config');

const router = express.Router();

const getBackendUrl = (endpoint) => `http://pepo_backend:5000${endpoint}`;

// Signup Route (GET)
router.get('/signup', (req, res) => {
  res.render('signup', { user: req.session.user, isProduction: config.isProduction });
});

// Signup Route (POST)
router.post('/signup', async (req, res) => {
  let { username, password, passcode } = req.body;

  username = username.trim();
  password = password.trim();

  // Validate username and password for spaces
  if (username.includes(' ') || password.includes(' ')) {
    return res.render('signup', { error: 'Username or Password cannot contain spaces', isProduction: config.isProduction });
  }
  
  // Production-specific passcode check
  if (config.isProduction && passcode !== config.signupPasscode) {
    return res.render('signup', { error: 'Incorrect passcode', isProduction: config.isProduction });
  }

  try {
    // Register the user via the backend service
    const response = await axios.post(getBackendUrl('/auth/register'), { username, password });

    if (response.status === 200 && response.data.message === 'User registered successfully') {
      req.session.user = {
        username: username,
        isAdmin: response.data.isAdmin || false  // Store isAdmin in session
      };
      req.session.token = response.data.token;  // Store the token in session
      res.redirect('/');
    }
  } catch (error) {
    if (error.response && error.response.status === 409) {
      // Username is already taken, show an error
      return res.render('signup', { error: 'Username is already taken', isProduction: config.isProduction });
    }
    console.error('Signup error:', error);
    res.status(500).send('Signup failed!');
  }
});

// Signin Route (GET)
router.get('/signin', (req, res) => {
  const error = req.query.error || null;
  res.render('signin', { error, user: req.session.user });
});

// Signin Route (POST)
router.post('/signin', async (req, res) => {
  const { username, password } = req.body;

  try {
    // Verify credentials via the backend service
    const response = await axios.post(getBackendUrl('/auth/verify_credentials'), { username, password });

    if (response.data.message === 'Credentials verified') {
      // Store user data in session
      req.session.user = {
        username: username,
        isAdmin: response.data.isAdmin || false  // Store isAdmin flag
      };
      req.session.token = response.data.token;  // Store the token in session
      req.session.save(err => {
        if (err) {
          res.redirect('/auth/signin?error=Session error');
        } else {
          res.redirect('/');
        }
      });
    } else {
      res.redirect('/auth/signin?error=Invalid username or password');
    }
  } catch (error) {
    console.error('Signin error:', error);
    res.redirect('/auth/signin?error=Invalid username or password');
  }
});

// Logout Route
router.get('/logout', (req, res) => {
  req.session.destroy(err => {
    if (err) {
      console.error('Logout error:', err);
      return res.redirect('/');
    }
    res.clearCookie('connect.sid');  // Clear the session cookie
    res.redirect('/auth/signin');
  });
});

module.exports = router;
