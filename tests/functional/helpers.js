const utilities = require('./utilities');
const generateToken = require('./jwt_helper');

const openQuestionnaire = (schema, { userId = utilities.getRandomString(10), collectionId = utilities.getRandomString(10), responseId = utilities.getRandomString(16), periodId = '201605', periodStr = 'May 2016', region = 'GB-ENG', language = 'en', sexualIdentity = false, includeLogoutUrl = false } = {}) => {
  return generateToken(schema, {userId, collectionId, responseId: responseId, periodId: periodId, periodStr: periodStr, regionCode: region, languageCode: language, sexualIdentity: sexualIdentity, includeLogoutUrl: includeLogoutUrl})
    .then(function(token) {
      browser.url('/session?token=' + token);
      return browser;
    });
};

module.exports = {
  openQuestionnaire
};
