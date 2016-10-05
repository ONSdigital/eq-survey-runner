import chai from 'chai'
import {getRandomString} from '../helpers'

const expect = chai.expect

describe('Error messages', function() {
  before('Progress to tge correct page', function() {
    const userId = '.qa-user-id'
    const collectionSID = '.qa-collection-sid'
    const selectSchema = '.qa-select-schema'
    browser.url('/dev')
    browser.waitForExist(userId)
    browser.setValue(userId, getRandomString(10))
    browser.waitForExist(collectionSID)
    browser.setValue(collectionSID, getRandomString(3))
    browser.waitForExist(selectSchema)
    browser.selectByValue(selectSchema, '1_0205.json')
    browser.click('.qa-btn-submit-dev')
    browser.click('.qa-btn-get-started')
    browser.setValue('[id="6fd644b0-798e-4a58-a393-a438b32fe637-day"]', '01')
    browser.setValue('[id="6fd644b0-798e-4a58-a393-a438b32fe637-year"]', '2016')
    browser.setValue('[id="06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day"]', '01')
    browser.setValue('[id="06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year"]', '2016')
    browser.click('.qa-btn-submit')
  })

  it('Error link is clicked to take focus to day input', function(done) {
    const inPageLink = browser.element('.js-inpagelink-trigger')
    inPageLink.waitForExist(10000)
    inPageLink.click()
    browser.timeoutsImplicitWait(10000)
    const activeElementValueNumber = browser.elementActive().value.ELEMENT
    const activeElementValue = browser.elementIdAttribute(activeElementValueNumber, "id").value
    expect(activeElementValue).to.contain('6fd644b0-798e-4a58-a393-a438b32fe637-day')
    browser.call(done)
  })

})
