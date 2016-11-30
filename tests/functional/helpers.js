import sampleSize from 'lodash/sampleSize'
import devPage from './pages/dev.page'
import landingPage from './pages/landing.page'

export const getUri = uri => browser.options.baseUrl + uri

export const getRandomString = length => sampleSize('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', length).join('')

export const openAndStartCensusQuestionnaire = (schema, sexualIdentity = false, region = 'GB-ENG') => {
  devPage.open()
    .setUserId(getRandomString(10))
    .setCollectionId(getRandomString(10))
    .setSchema(schema)
    .setRegionCode(region)

  if (sexualIdentity) {
    devPage.checkSexualIdentity()
  }

  devPage.submit()
  landingPage.getStarted()
}

export const openQuestionnaire = (schema, userId = getRandomString(10), collectionId = getRandomString(10)) => {
  devPage.open()
    .setUserId(userId)
    .setCollectionId(collectionId)
    .setSchema(schema)
    .submit()
}

export const startQuestionnaire = (schema, userId = getRandomString(10), collectionId = getRandomString(10)) => {
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
