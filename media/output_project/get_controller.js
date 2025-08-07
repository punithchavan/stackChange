const express = require('express');
const router = express.Router();

router.get('/:post_id', async (req, res) => {
try {
const post = await Post.findById(req.params.post_id);
if (!post) {
return res.status(404).json({ error: 'Post not found' });
}
res.json({ author: post.author.username, content: post.content, createdAt: post.createdAt });
} catch (error) {
res.status(500).json({ error: 'Server error' });
}
});


module.exports = router;