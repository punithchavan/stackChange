const express = require('express');
const router = express.Router();

router.post('/tweets', (req, res) => {
res.json({ msg: 'Tweet Created' });
});


router.delete('/tweet', (req, res) => {
res.json({ msg: 'Tweet Deleted' });
});


module.exports = router;