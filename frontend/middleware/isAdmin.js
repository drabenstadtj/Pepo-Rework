const isAdmin = (req, res, next) => {
    if (req.session && req.session.user && req.session.user.isAdmin) {
      return next();  // User is admin, proceed to the next middleware/route handler
    } else {
      res.status(403).send('Access denied. Admins only.');
    }
  }
    module.exports = isAdmin;