import chai from 'chai'
import {getRandomString} from '../helpers'

const expect = chai.expect

describe('RSI - Save and restore test', function() {
  before('Progress from the developer page', function() {
    const userId = '.qa-user-id'
    const collectionSID = '.qa-collection-sid'
    const selectSchema = '.qa-select-schema'
    const periodID = 'period_id'
    const periodString = '.period_str'
    browser.url('/dev')
    browser.waitForExist(userId)
    browser.setValue(userId, 'yoganandkunche')
    browser.waitForExist(collectionSID)
    browser.setValue(collectionSID, '7890102')
    browser.setValue(periodID, '7890102')
    browser.setValue(periodString, '7890102')
    browser.waitForExist(selectSchema)
    browser.selectByValue(selectSchema, '1_0102.json')
    browser.debug()
    browser.click('.qa-btn-submit-dev')
  })
