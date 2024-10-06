const express = require('express');
const session = require('express-session');
const path = require('path');
const morgan = require('morgan');
const config = require('./config/config');

const app = express();

// Set the view engine to Pug and specify the views directory
app.set('view engine', 'pug');
app.set('views', path.join(__dirname, 'views'));

// Middleware to parse URL-encoded bodies and serve static files
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

// Configure session middleware
app.use(session({
  secret: config.sessionSecret,
  resave: false,
  saveUninitialized: true,
  cookie: {
    httpOnly: true,
    secure: config.isProduction,
    sameSite: config.isProduction ? 'None' : 'Lax',
    maxAge: 24 * 60 * 60 * 1000  // Cookie expiration time
  }
}));

// Add request logging
app.use(morgan('combined'));

// Register routes
const authRoutes = require('./routes/auth');
const indexRoutes = require('./routes/index');
const leaderboardRoutes = require('./routes/leaderboard');
const stocksRoutes = require('./routes/stocks');
const tradeRoutes = require('./routes/trade');
const portfolioRoutes = require('./routes/portfolio');
const adminRoutes = require('./routes/admin');
const shopRouter = require('./routes/shop'); // Adjust the path as needed

app.use('/auth', authRoutes);
app.use('/', indexRoutes);
app.use('/leaderboard', leaderboardRoutes);
app.use('/stocks', stocksRoutes);
app.use('/trade', tradeRoutes);
app.use('/portfolio', portfolioRoutes);
app.use('/admin', adminRoutes);
app.use('/shop', shopRouter);

// Error handling
app.use((err, req, res, next) => {
  console.error('Internal Server Error:', err);
  res.status(500).send('Internal Server Error');
});

if (config.isProduction) {
  app.listen(3000, () => {
    console.log(`Server is running in production mode on http://localhost:3000`);
  });
} else {
  app.listen(3000, () => {
    console.log(`Server is running in development mode on http://localhost:3000`);
  });
}
