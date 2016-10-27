import sampleSize from 'lodash/sampleSize'
import devPage from './pages/dev.page'
import landingPage from './pages/landing.page'

export const getUri = uri => browser.options.baseUrl + uri

export const getRandomString = length => sampleSize('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', length).join('')

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
    return browser.elementIdAttribute(element.value.ELEMENT, "id").value
  }
