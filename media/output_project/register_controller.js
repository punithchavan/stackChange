const express = require('express');
const router = express.Router();
const User = require('./user'); // Assuming User model is defined elsewhere

router.post('/register', async (req, res) => {
try {
const user = await User.create({ username: req.body.username, password: req.body.password });
res.json({ message: 'User registered successfully' });
} catch (error) {
res.status(400).json({ error: 'User already exists' });
}
});


module.exports = router;