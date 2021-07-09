const mongoose = require('mongoose')
const Schema = mongoose.Schema

Const Album = new Schema(
    {
        title: { type: String, required: true},
        release: { type: [String], required: true},
    },
    { timestamps: true},
)

module.exports = mongoose.model('albums', Album)
