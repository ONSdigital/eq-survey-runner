const _ = require('lodash');

const getRandomString = length => _.sampleSize('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', length).join('');

module.exports = {
  getRandomString,
};
