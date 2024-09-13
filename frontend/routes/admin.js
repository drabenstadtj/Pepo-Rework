const express = require('express');
const axios = require('axios');
const isAdmin = require('../middleware/isAdmin');
const router = express.Router();

const getBackendUrl = (endpoint) => `http://pepo_backend:5000${endpoint}`;

// Render the admin dashboard
router.get('/', isAdmin, (req, res) => {
  res.render('admin', { user: req.session.user });
});

// Handle the tester entry insertion
router.post('/add-tester', isAdmin, async (req, res) => {
  try {
    // Define the tester entry
    const testerEntry = {
      title: "Breaking News: Tech Stocks Soar",
      content: "Tech stocks surged today, with major gains in the software sector. Analysts attribute the rise to recent earnings reports that exceeded expectations.",
      author: "Jane Doe",
      timestamp: new Date(),
      isFeatured: true,
      thumbnail: "https://example.com/image.jpg"
    };

    // Send a POST request to the backend to insert the entry
    await axios.post(getBackendUrl('/news'), testerEntry);

    // Redirect back to the admin dashboard with a success message
    res.redirect('/admin?success=Tester entry added');
  } catch (error) {
    console.error("Error adding tester entry:", error);
    res.redirect('/admin?error=Failed to add tester entry');
  }
});

module.exports = router;
