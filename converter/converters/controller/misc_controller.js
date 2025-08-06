const express = require('express');
const router = express.Router();

router.post('/login', (req, res) => {
res.json({ msg: 'Login Successful' });
});


router.post('/register', (req, res) => {
res.json({ msg: 'User Registered' });
});


module.exports = router;