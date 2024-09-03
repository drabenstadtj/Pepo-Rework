const attachToken = (req, res, next) => {
    if (req.session && req.session.token) {
      req.headers['Authorization'] = `Bearer ${req.session.token}`;
    }
    next();
  };
  
  module.exports = attachToken;
  