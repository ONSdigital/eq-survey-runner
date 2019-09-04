const utilities = require('./utilities');
const IntroductionPage = require('./base_pages/introduction.page');
const genericPage = require('./base_pages/generic.page');
const generateToken = require('./jwt_helper');

const introductionPage = new IntroductionPage('introduction');

const getUri = uri => browser.options.baseUrl + uri;

const openCensusQuestionnaire = (schema, sexualIdentity = false, region = 'GB-ENG', language = 'en') => {
  return generateToken(schema, {userId: utilities.getRandomString(10), collectionId: utilities.getRandomString(10), periodId: '2011', periodStr: null, regionCode: region, languageCode: language, sexualIdentity: sexualIdentity, country: 'E', displayAddress: '68 Abingdon Road, Goathill'})
    .then(function(token) {
      return browser.url('/session?token=' + token);
    });
};

const startCensusQuestionnaire = (schema, sexualIdentity = false, region = 'GB-ENG', language = 'en') => {
  return openCensusQuestionnaire(schema, sexualIdentity, region, language).then(() => {
      return browser.click(introductionPage.getStarted());
  });
};

function openQuestionnaire(schema, { userId = utilities.getRandomString(10), collectionId = utilities.getRandomString(10), responseId = utilities.getRandomString(16), periodId = '201605', periodStr = 'May 2016', region = 'GB-ENG', language = 'en', sexualIdentity = false, includeLogoutUrl = false, displayAddress='68 Abingdon Road, Goathill'} = {}) {
  return generateToken(schema, {userId, collectionId, responseId: responseId, periodId: periodId, periodStr: periodStr, regionCode: region, languageCode: language, sexualIdentity: sexualIdentity, includeLogoutUrl: includeLogoutUrl, displayAddress: displayAddress})
    .then(function(token) {
      return browser.url('/session?token=' + token);
    });
}

function startQuestionnaire(schema, userId = utilities.getRandomString(10), collectionId = utilities.getRandomString(10)) {
  return openQuestionnaire(schema, userId, collectionId).then(() => {
      return browser.click(introductionPage.getStarted());
  });
}

function getElementId(element) {
  return browser.elementIdAttribute(element.value.ELEMENT, 'id').value;
}

function setMobileViewport() {
  return browser.setViewportSize({
    width: 320,
    height: 568
  });
}

function pressSubmit(numberOfTimes) {
    let chain = browser
          .click(genericPage.submit());

    for (var i = 0; i < (numberOfTimes -1); i++) {
      chain = chain.then(() => {
        return browser
          .click(genericPage.submit());
      });
    }
    return chain;
 }

module.exports = {
  introductionPage,
  getUri,
  openCensusQuestionnaire,
  startCensusQuestionnaire,
  openQuestionnaire,
  startQuestionnaire,
  getElementId,
  setMobileViewport,
  pressSubmit
};
