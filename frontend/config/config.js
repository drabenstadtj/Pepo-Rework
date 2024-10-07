const path = require('path');
const dotenv = require('dotenv');

// Load environment variables from .env file
dotenv.config({ path: path.resolve(__dirname, '../.env') });

const requiredEnvVars = [
  'SECRET_KEY',
  'SESSION_SECRET',
  'MODE',
  'BACKEND_URL',
  'SIGNUP_PASSCODE',
];

const config = {
  isProduction: process.env.MODE === 'production',  // Use MODE for consistency
  secretKey: process.env.SECRET_KEY,
  sessionSecret: process.env.SESSION_SECRET,
  apiUrl: process.env.BACKEND_URL,  // Ensure API URL is configurable
  signupPasscode: process.env.SIGNUP_PASSCODE,
};

// Validate necessary environment variables
requiredEnvVars.forEach((varName) => {
  if (!process.env[varName]) {
    console.error(`Error: ${varName} is not set in the environment variables.`);
    process.exit(1);
  }
});

module.exports = config;
