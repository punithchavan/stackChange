const mongoose = require('mongoose');

const PostSchema = new mongoose.Schema({
  author: {
    "type": "mongoose.Schema.Types.ObjectId",
    "ref": "User"
},
  content: {
    "type": "String",
    "required": true
},
}, { timestamps: true });

module.exports = mongoose.model('Post', PostSchema);
