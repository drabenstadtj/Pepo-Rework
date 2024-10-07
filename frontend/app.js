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
  secret: config.secretKey,
  resave: false,
  saveUninitialized: true,
  cookie: {
    httpOnly: true,
    secure: config.isProduction,  // Ensure secure cookies in production
    sameSite: config.isProduction ? 'None' : 'Lax',
    maxAge: 24 * 60 * 60 * 1000  // 1 day
  }
}));


// Add request logging
app.use(morgan('combined'));

// Pass apiUrl to all views
app.use((req, res, next) => {
  res.locals.apiUrl = config.apiUrl;
  next();
});

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
  if (req.xhr || req.headers.accept.indexOf('json') > -1) {
    res.status(500).json({ message: 'Internal Server Error' });
  } else {
    res.status(500).send('Internal Server Error');
  }
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running in ${config.isProduction ? 'production' : 'development'} mode on http://localhost:${PORT}`);
});
