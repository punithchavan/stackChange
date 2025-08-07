const express = require('express');
const router = express.Router();
const User = require('../models/User');
const Post = require('../models/Post');

router.post('/create_post', async (req, res) => {
try {
const user = await User.findById(req.body.user_id);
if (!user) {
return res.status(400).json({ error: 'User not found' });
}
const post = await Post.create({ author: user._id, content: req.body.content });
res.json({ message: 'Post created', post_id: post._id });
} catch (error) {
res.status(400).json({ error: 'Error creating post' });
}
});


module.exports = router;