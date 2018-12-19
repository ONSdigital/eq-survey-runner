const _ = require('lodash')
const jwthelper = require('./jwt_helper.js') //import {generateToken} from './jwt_helper.js'

const getRandomString = length => _.sampleSize('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', length).join('');

function getToken(schema, { userId = getRandomString(10), collectionId = getRandomString(10), periodId = '201605', periodStr = 'May 2016', region = 'GB-ENG', language = 'en', sexualIdentity = false, includeLogoutUrl = false } = {}) {
  return jwthelper.generateToken(schema, userId, collectionId, periodId, periodStr, region, language, sexualIdentity, includeLogoutUrl)
}

/*
function openQuestionnaire(schema, { userId = getRandomString(10), collectionId = getRandomString(10), periodId = '201605', periodStr = 'May 2016', region = 'GB-ENG', language = 'en', sexualIdentity = false, includeLogoutUrl = false } = {}) {
  return jwthelper.generateToken(schema, userId, collectionId, periodId, periodStr, region, language, sexualIdentity, includeLogoutUrl).then((token) => {
      return cy.visit('/session?token=' + token);
  })
}

*/

function openQuestionnaire(schema, { userId = getRandomString(10), collectionId = getRandomString(10), periodId = '201605', periodStr = 'May 2016', region = 'GB-ENG', language = 'en', sexualIdentity = false, includeLogoutUrl = false } = {}) {
  return cy
    .then(()=> {return jwthelper.generateToken(schema, userId, collectionId, periodId, periodStr, region, language, sexualIdentity, includeLogoutUrl)})
    .then((token) => {
      return cy.visit('/session?token=' + token)
    })
}

function startQuestionnaire(schema, userId = getRandomString(10), collectionId = getRandomString(10)) {
  return openQuestionnaire(schema, userId, collectionId)
         .get('.qa-btn-get-started').click()
}

function isSectionComplete(linkName) {
  return cy
    .get(navigationLink(linkName))
    .then(($elem)=> {
      const dataQa = $elem.attr('data-qa')
      return dataQa === 'complete'
    })
}

module.exports = {
  openQuestionnaire,
  getToken,
  isSectionComplete,
  startQuestionnaire,
};
