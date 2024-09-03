const express = require('express');
const axios = require('axios');
const config = require('../config/config');

const router = express.Router();

const getBackendUrl = (endpoint) => `http://localhost:${config.backendPort}${endpoint}`;

router.get('/signup', (req, res) => {
  res.render('signup', { user: req.session.user, isProduction: config.isProduction });
});

router.post('/signup', async (req, res) => {
  const { username, password, passcode } = req.body;

  if (config.isProduction && passcode !== config.signupPasscode) {
    return res.render('signup', { error: 'Incorrect passcode', isProduction: config.isProduction });
  }

  try {
    const response = await axios.post(getBackendUrl('/auth/register'), { username, password });
    if (response.data.message === 'User registered successfully') {
      req.session.user = username;
      req.session.token = response.data.token;
      res.redirect('/');
    } else {
      res.send('Signup failed!');
    }
  } catch (error) {
    console.error('Signup error:', error);
    res.status(500).send('Signup failed!');
  }
});

router.get('/signin', (req, res) => {
  const error = req.query.error;
  res.render('signin', { error, user: req.session.user });
});

router.post('/signin', async (req, res) => {
  const { username, password } = req.body;
  try {
    const response = await axios.post(getBackendUrl('/auth/verify_credentials'), { username, password });
    if (response.data.message === 'Credentials verified') {
      req.session.user = username;
      req.session.token = response.data.token;
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

router.get('/logout', (req, res) => {
  req.session.destroy(err => {
    if (err) {
      console.error('Logout error:', err);
      return res.redirect('/');
    }
    res.clearCookie('connect.sid');
    res.redirect('/auth/signin');
  });
});

module.exports = router;
