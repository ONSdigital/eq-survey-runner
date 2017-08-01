import {sampleSize} from 'lodash'
import landingPage from './pages/landing.page'
import {generateToken} from './jwt_helper'

export {landingPage}

export const getRandomString = length => sampleSize('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', length).join('')

export const startCensusQuestionnaire = (schema, sexualIdentity = false, region = 'GB-ENG', language = 'en') => {
  generateToken(schema, getRandomString(10), getRandomString(10), null, null, region, language, sexualIdentity)
    .then(function(token) {
      return browser.url('/session?token=' + token)
    })

  browser.pause(2000) // Double Shudder!!!
}

export function openQuestionnaire(schema, userId = getRandomString(10), collectionId = getRandomString(10), periodId = '201605', periodStr = 'May 2016') {
  generateToken(schema, userId, collectionId, periodId, periodStr)
    .then(function(token) {
      return browser.url('/session?token=' + token)
    })

  browser.pause(2000) // Double Shudder!!!
}

export function startQuestionnaire(schema, userId = getRandomString(10), collectionId = getRandomString(10)) {
  openQuestionnaire(schema, userId, collectionId)

  landingPage.getStarted()
}

export function getElementId(element) {
  return browser.elementIdAttribute(element.value.ELEMENT, 'id').value
}

export const getBlockId = () => {
  return getLocation().blockId
}

export const getRepeatedGroup = () => {
  return getLocation().repeatedGroup
}

export const getLocation = () => {
  // Matches: /(groupId)/(blockId)
  var regexp = /questionnaire.+\/(\d+)\/(.+)$/g
  var matches = regexp.exec(browser.getUrl())

  if (matches != null) {
    return {
      'repeatedGroup': matches[1],
      'blockId': matches[2]
    }
  }
}

export const setMobileViewport = () => {
  return browser.setViewportSize({
    width: 320,
    height: 568
  })
}

export const openMobileNavigation = () => {
  browser.click('#menu-btn')
  return browser.waitUntil(function() {
    return browser.isVisibleWithinViewport('#section-nav')
  })
}

export const closeMobileNavigation = () => {
  browser.pause(100)
  browser.click('#menu-btn')
  browser.pause(200)
  return browser.waitUntil(function() {
    return !browser.isVisibleWithinViewport('#section-nav')
  })
}

export const isViewSectionsVisible = () => {
  let viewSectionsLink = '#menu-btn'
  return browser.isExisting(viewSectionsLink) && browser.isVisibleWithinViewport(viewSectionsLink)
}
