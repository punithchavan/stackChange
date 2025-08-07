const express = require('express');
const router = express.Router();
const Post = require('../models/Post');
const User = require('../models/User');
const Comment = require('../models/Comment');

router.post('/add_comment', async (req, res) => {
try {
const post = await Post.findById(req.body.post_id);
const user = await User.findById(req.body.user_id);
const comment = await Comment.create({ post: post._id, user: user._id, comment_text: req.body.comment_text });
res.json({ message: 'Comment added', comment_id: comment._id });
} catch (error) {
res.status(400).json({ error: 'Invalid post or user' });
}
});


module.exports = router;