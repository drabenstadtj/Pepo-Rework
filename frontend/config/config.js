const path = require('path');
const dotenv = require('dotenv');

dotenv.config({ path: path.resolve(__dirname, '../.env') });

const config = {
  isProduction: process.env.CONFIG === 'production',
  secretKey: process.env.SECRET_KEY,
  sessionSecret: process.env.SESSION_SECRET,
  signupPasscode: process.env.SIGNUP_PASSCODE,
};

if (!config.secretKey) {
  console.error('Error: SECRET_KEY is not set in the environment variables.');
  process.exit(1);
}

if (!config.sessionSecret) {
  console.error('Error: SESSION_SECRET is not set in the environment variables.');
  process.exit(1);
}

module.exports = config;
