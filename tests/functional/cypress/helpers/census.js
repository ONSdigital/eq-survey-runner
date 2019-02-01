const _ = require('lodash');
const generateToken = require('../../jwt_helper');

const getUri = uri => cy.config.baseUrl + uri;

const getRandomString = length => _.sampleSize('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', length).join('');

const openCensusQuestionnaire = (schema, sexualIdentity = false, region = 'GB-ENG', language = 'en') => {
  return cy
    .then(() => {
      return generateToken(schema, {userId: getRandomString(10), collectionId: getRandomString(10), periodId: '2011', periodStr: null, regionCode: region, languageCode: language, sexualIdentity: sexualIdentity, country: 'E', displayAddress: '68 Abingdon Road, Goathill'});
    })
    .then(function(token) {
      return cy.visit('/session?token=' + token);
    });
};

module.exports = {
  getUri,
  getRandomString,
  openCensusQuestionnaire
};
