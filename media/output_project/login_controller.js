const express = require('express');
const router = express.Router();

router.post('/login', (req, res) => {
const { username, password } = req.body;
// Replace with your actual authentication logic
const user = authenticate(username, password);
if (user) {
res.json({ message: 'Login successful', user_id: user.id, token: 'dummy-jwt-token' });
} else {
res.status(401).json({ error: 'Invalid credentials' });
}
});


function authenticate(username, password) {
// Replace with your actual authentication logic.  This is a placeholder.
if (username === 'testuser' && password === 'password') {
return { id: 1 };
}
return null;
}

module.exports = router;