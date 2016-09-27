import assert from 'assert'
import chai from 'chai'
import {getRandomString} from '../helpers'

const expect = chai.expect

describe('RSI - Save and restore test', function() {
  before('Progress from the developer page for 1_0102', function() {
    const userId = '.qa-user-id'
    const collectionSID = '.qa-collection-sid'
    const selectSchema = '.qa-select-schema'
    browser.url('/dev')
    browser.windowHandleMaximize()
    browser.deleteCookie()
    browser.waitForExist(userId)
    browser.setValue(userId, getRandomString(3))
    browser.waitForExist(collectionSID)
    browser.setValue(collectionSID, getRandomString(3))
    browser.waitForExist(selectSchema)
    browser.selectByValue(selectSchema, '1_0102.json')
    browser.click('.qa-btn-submit-dev')
  })

  it('The landing page has been reached', function(done) {
    const getStartedBtn = browser.element('.qa-btn-get-started')
    getStartedBtn.waitForExist(10000)
    const url = browser.url().value
    expect(url).to.contain('introduction')
    getStartedBtn.click()
  })

  it('The questionnaire page has been reached', function(done) {
    const questionnaireElementExists = browser.isExisting('.qa-questionnaire-form')
    expect(questionnaireElementExists).to.equal(true)
  })

  it('Entering data in form', function(done) {
    const questionnaireElementExists = browser.isExisting('.qa-questionnaire-form')
    expect(questionnaireElementExists).to.equal(true)
    const submitBtn = browser.element('.qa-btn-submit')
    submitBtn.waitForExist(10000)
    browser.setValue('[id = "94f368e4-7c6c-4272-a780-8c46328626a2-year"]', '2016')
    browser.setValue('#dc156715-3d48-4af3-afed-7a0a6bb65583-year', '2017')
    browser.element('.qa-btn-submit').click();
    browser.setValue('.input--currency', '12345')
    browser.element('.qa-btn-submit').click();
    browser.setValue('.input--currency', '1234')
    browser.element('.qa-btn-submit').click();
    browser.setValue('.input--textarea', 'This is to test edit links on summary screen')
    browser.element('.qa-btn-submit').click();
    browser.debug()
  })
})
