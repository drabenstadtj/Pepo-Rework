const path = require('path');
const dotenv = require('dotenv');

// Load environment variables from .env file
dotenv.config({ path: path.resolve(__dirname, '../.env') });

const config = {
  isProduction: process.env.NODE_ENV === 'production',  // Use NODE_ENV for consistency
  secretKey: process.env.SECRET_KEY,
  sessionSecret: process.env.SESSION_SECRET,
  apiUrl: process.env.API_URL || 'http://localhost:5000',  // Ensure API URL is configurable
  signupPasscode: process.env.SIGNUP_PASSCODE,
};

// Validate necessary environment variables
if (!config.secretKey) {
  console.error('Error: SECRET_KEY is not set in the environment variables.');
  process.exit(1);
}

if (!config.sessionSecret) {
  console.error('Error: SESSION_SECRET is not set in the environment variables.');
  process.exit(1);
}

module.exports = config;
