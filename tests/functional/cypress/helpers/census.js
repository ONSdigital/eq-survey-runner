const _ = require('lodash');
const utilities = require('../../utilities');
const generateToken = require('../../jwt_helper');

const getUri = uri => cy.config.baseUrl + uri;

const openCensusQuestionnaire = (schema, sexualIdentity = false, region = 'GB-ENG', language = 'en') => {
  return cy
    .then(() => {
      return generateToken(schema, {userId: utilities.getRandomString(10), collectionId: utilities.getRandomString(10), periodId: '2011', periodStr: null, regionCode: region, languageCode: language, sexualIdentity: sexualIdentity, country: 'E', displayAddress: '68 Abingdon Road, Goathill'});
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
