const express = require('express');
const router = express.Router();

// Import Controller Functions (grouped by model)
const {
  createadd_comment,
  createcreate_post,
  createlogin_user,
  createregister_user,
  deleteget_post,
  getadd_comments,
  getcreate_posts,
  getget_post,
  getlogin_users,
  getregister_users,
  updateget_post
} = require('../controllers/genericController');

// --- API Routes ---
router.delete('/posts/:post_id/', deleteget_post);
router.get('/comments/', getadd_comments);
router.get('/login/', getlogin_users);
router.get('/posts/', getcreate_posts);
router.get('/posts/:post_id/', getget_post);
router.get('/register/', getregister_users);
router.post('/comments/', createadd_comment);
router.post('/login/', createlogin_user);
router.post('/posts/', createcreate_post);
router.post('/register/', createregister_user);
router.put('/posts/:post_id/', updateget_post);

module.exports = router;
