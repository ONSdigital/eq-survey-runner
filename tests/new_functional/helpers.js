const _ = require('lodash');
const landingPage = require('./pages/landing.page');
const generateToken = require('./jwt_helper');

const getUri = uri => browser.options.baseUrl + uri;

const getRandomString = length => _.sampleSize('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', length).join('');

const startCensusQuestionnaire = (schema, sexualIdentity = false, region = 'GB-ENG', language = 'en') => {
  return generateToken(schema, getRandomString(10), getRandomString(10), null, null, region, language, sexualIdentity)
    .then(function(token) {
      return browser.url('/session?token=' + token);
    });
};

function openQuestionnaire(schema, userId = getRandomString(10), collectionId = getRandomString(10), periodId = '201605', periodStr = 'May 2016') {
  return generateToken(schema, userId, collectionId, periodId, periodStr)
    .then(function(token) {
      return browser.url('/session?token=' + token);
    });
}

function startQuestionnaire(schema, userId = getRandomString(10), collectionId = getRandomString(10)) {
  return openQuestionnaire(schema, userId, collectionId).then(() => {
      return browser.click(landingPage.getStarted());
  });
}

function getElementId(element) {
  return browser.elementIdAttribute(element.value.ELEMENT, 'id').value;
}

function getBlockId() {
  return getLocation().blockId;
}

function getRepeatedGroup() {
  return getLocation().repeatedGroup;
}

function getLocation() {
  // Matches: /(groupId)/(blockId)
  var regexp = /questionnaire.+\/(\d+)\/(.+)$/g;
  var matches = regexp.exec(browser.getUrl());

  if (matches != null) {
    return {
      'repeatedGroup': matches[1],
      'blockId': matches[2]
    };
  }

  return undefined;
}

function setMobileViewport() {
  return browser.setViewportSize({
    width: 320,
    height: 568
  });
}

function openMobileNavigation() {
  browser.click('#menu-btn');
  return browser.waitUntil(function() {
    return browser.isVisibleWithinViewport('#section-nav');
  });
}

function closeMobileNavigation() {
  browser.pause(100);
  browser.click('#menu-btn');
  browser.pause(200);
  return browser.waitUntil(function() {
    return !browser.isVisibleWithinViewport('#section-nav');
  });
}

function isViewSectionsVisible() {
  let viewSectionsLink = '#menu-btn';
  return browser.isExisting(viewSectionsLink) && browser.isVisibleWithinViewport(viewSectionsLink);
}

function navigationLink(linkName) {
    return 'a=' + linkName
}

function isSectionComplete(linkName) {
    return isSectionCompleteBind.bind(null, linkName)
}

function isSectionCompleteBind(linkName) {
  return browser
    .element(navigationLink(linkName))
    .getAttribute('data-qa')
    .then(function (data_qa_string) {
      if (data_qa_string === 'complete') {
        return true
      }
      return false
    });
}

module.exports = {
  landingPage,
  getUri,
  getRandomString,
  startCensusQuestionnaire,
  openQuestionnaire,
  startQuestionnaire,
  getElementId,
  getBlockId,
  getRepeatedGroup,
  getLocation,
  setMobileViewport,
  openMobileNavigation,
  closeMobileNavigation,
  isViewSectionsVisible,
  navigationLink,
  isSectionComplete
}
