const express = require('express');
const axios = require('axios');
const config = require('../config/config');
const isAdmin = require('../middleware/isAdmin');

const router = express.Router();

const getBackendUrl = (endpoint) => `http://localhost:5000/${endpoint}`;

router.get('/', isAdmin, (req, res) => {
    res.render('admin', { user: req.session.user });
});
  
module.exports = router;