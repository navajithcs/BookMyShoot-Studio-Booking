const mongoose = require('mongoose');

const locationSchema = new mongoose.Schema({
  state: {
    type: String,
    required: [true, 'State is required'],
    trim: true
  },
  district: {
    type: String,
    required: [true, 'District is required'],
    trim: true
  },
  latitude: {
    type: String,
    required: [true, 'Latitude is required']
  },
  longitude: {
    type: String,
    required: [true, 'Longitude is required']
  },
  createdAt: {
    type: Date,
    default: Date.now
  }
});

// Index for faster geospatial-like querying if needed
locationSchema.index({ state: 1, district: 1 });

module.exports = mongoose.model('Location', locationSchema);
