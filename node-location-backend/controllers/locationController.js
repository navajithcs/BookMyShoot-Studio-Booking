const Location = require('../models/Location');
const axios = require('axios');

// Cache for India Data
let indiaDataCache = null;

const fetchIndiaData = async () => {
  if (indiaDataCache) return indiaDataCache;
  try {
    const response = await axios.get('https://raw.githubusercontent.com/ashishjain1988/india-states-cities-list/master/cities.json');
    indiaDataCache = response.data;
    return indiaDataCache;
  } catch (error) {
    console.error("Failed to fetch India states/cities data", error);
    throw new Error("Unable to load states and districts data");
  }
};

// @desc    Save user location
// @route   POST /api/location
exports.saveLocation = async (req, res, next) => {
  try {
    const { state, district, lat, lon } = req.body;

    if (!state || !district || !lat || !lon) {
      return res.status(400).json({ success: false, message: 'Please provide state, district, lat, and lon' });
    }

    const location = await Location.create({
      state,
      district,
      latitude: lat,
      longitude: lon
    });

    res.status(201).json({
      success: true,
      data: location
    });
  } catch (error) {
    next(error);
  }
};

// @desc    Get all Indian states
// @route   GET /api/states
exports.getStates = async (req, res, next) => {
  try {
    const data = await fetchIndiaData();
    const states = Object.keys(data);
    
    res.status(200).json({
      success: true,
      count: states.length,
      data: states
    });
  } catch (error) {
    next(error);
  }
};

// @desc    Get districts by state
// @route   GET /api/districts/:state
exports.getDistrictsByState = async (req, res, next) => {
  try {
    const data = await fetchIndiaData();
    const state = req.params.state;
    
    const districts = data[state];
    
    if (!districts) {
      return res.status(404).json({ success: false, message: `No districts found for state: ${state}` });
    }

    res.status(200).json({
      success: true,
      count: districts.length,
      data: districts
    });
  } catch (error) {
    next(error);
  }
};

// @desc    Get saved location by ID
// @route   GET /api/location/:id
exports.getLocationById = async (req, res, next) => {
  try {
    const location = await Location.findById(req.params.id);

    if (!location) {
      return res.status(404).json({ success: false, message: 'Location not found' });
    }

    res.status(200).json({
      success: true,
      data: location
    });
  } catch (error) {
    next(error);
  }
};
