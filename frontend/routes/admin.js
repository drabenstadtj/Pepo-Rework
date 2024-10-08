const express = require('express');
const axios = require('axios');
const requireLogin = require('../middleware/requireLogin');  // Combined middleware
const router = express.Router();

const getBackendUrl = (endpoint) => `http://pepo_backend:5000${endpoint}`;

// Admin Dashboard Route
router.get('/', requireLogin, async (req, res) => {
    try {
        if (!req.user.isAdmin) {
            return res.status(403).send('Access denied. Admins only.');
        }

        // Fetch all stocks
        const response = await axios.get(getBackendUrl('/stocks/list'));

        // Get the success or error message from query params
        const success = req.query.success || null;
        const error = req.query.error || null;

        // Render the admin page with stocks, success, and error messages
        res.render('admin', {
            user: req.user,  // Use req.user from requireLogin middleware
            stocks: response.data,
            success,
            error
        });
    } catch (error) {
        console.error('Error fetching stock list:', error);
        res.redirect('/admin?error=Unable to fetch stock data');
    }
});

// Update Stock Volatility Route
router.post('/stocks/:symbol/update_volatility', requireLogin, async (req, res) => {
    try {
        if (!req.user.isAdmin) {
            return res.status(403).send('Access denied. Admins only.');
        }

        const { symbol } = req.params;
        const { volatility_factor } = req.body;

        await axios.post(getBackendUrl(`/admin/stocks/${symbol}/update_volatility`), {
            volatility_factor: parseFloat(volatility_factor)
        });

        // Redirect back to the admin page with a success message
        res.redirect(`/admin?success=Volatility updated for ${symbol}`);
    } catch (error) {
        console.error(`Error updating stock volatility for ${symbol}:`, error);
        res.redirect(`/admin?error=Failed to update volatility for ${symbol}`);
    }
});

// Add News Article Route
router.post('/add-news', requireLogin, async (req, res) => {
    try {
        if (!req.user.isAdmin) {
            return res.status(403).send('Access denied. Admins only.');
        }

        const { title, content, author, timestamp, isFeatured, thumbnail } = req.body;

        // Prepare the data to send to the backend
        const newsEntry = {
            title: title.trim(),
            content: content.trim(),
            author: author.trim(),
            timestamp: new Date(timestamp),
            isFeatured: !!isFeatured,  // Convert checkbox value to boolean
        };

        // Only add the thumbnail if it's provided
        if (thumbnail && thumbnail.trim()) {
            newsEntry.thumbnail = thumbnail.trim();
        }

        // Send a POST request to the backend to insert the news entry
        await axios.post(getBackendUrl('/news'), newsEntry);

        // Redirect back to the admin dashboard with a success message
        res.redirect('/admin?success=News article added successfully');
    } catch (error) {
        console.error("Error adding news article:", error);
        res.redirect('/admin?error=Failed to add news article');
    }
});

module.exports = router;
