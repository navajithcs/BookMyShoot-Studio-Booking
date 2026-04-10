const express = require('express');
const {
  saveLocation,
  getStates,
  getDistrictsByState,
  getLocationById
} = require('../controllers/locationController');

const router = express.Router();

router.post('/location', saveLocation);
router.get('/states', getStates);
router.get('/districts/:state', getDistrictsByState);
router.get('/location/:id', getLocationById);

module.exports = router;
