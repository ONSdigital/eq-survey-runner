const utilities = require('./utilities');
const IntroductionPage = require('./base_pages/introduction.page');
const genericPage = require('./base_pages/generic.page');
const generateToken = require('./jwt_helper');
const introductionPage = new IntroductionPage('introduction');

const openQuestionnaire = (schema, { userId = utilities.getRandomString(10), collectionId = utilities.getRandomString(10), responseId = utilities.getRandomString(16), periodId = '201605', periodStr = 'May 2016', region = 'GB-ENG', language = 'en', sexualIdentity = false, includeLogoutUrl = false } = {}) => {
  return generateToken(schema, {userId, collectionId, responseId: responseId, periodId: periodId, periodStr: periodStr, regionCode: region, languageCode: language, sexualIdentity: sexualIdentity, includeLogoutUrl: includeLogoutUrl})
    .then(function(token) {
      browser.url('/session?token=' + token);
      return browser;
    });
}

module.exports = {
  openQuestionnaire
};
