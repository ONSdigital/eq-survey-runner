import chai from 'chai'
import {getRandomString} from '../helpers'

const expect = chai.expect

describe('MCI test', function() {
  before('Progress from the developer page', function() {
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
  })

  it('The landing page has been reached', function() {
    const getStartedBtn = browser.element('.qa-btn-get-started')
    getStartedBtn.waitForExist(10000)
    const url = browser.url().value
    expect(url).to.contain('introduction')
    getStartedBtn.click()
  })

  it('The questionnaire page has been reached', function() {
    const questionnaireElementExists = browser.isExisting('.qa-questionnaire-form')
    expect(questionnaireElementExists).to.equal(true)
  })

  it('The form can be filled in and submitted', function() {
    const submitBtn = browser.element('.qa-btn-submit')
    submitBtn.waitForExist(10000)
    browser.setValue('#6fd644b0-798e-4a58-a393-a438b32fe637-year', '2016')
    browser.setValue('#06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year', '2017')
    browser.setValue('.input-type--currency .input', 2000)
    submitBtn.click()
    const url = browser.url().value
    expect(url).to.contain('summary')
  })

  it('The survey can be completed with "thankyou page" reached', function() {
    const submitBtn = browser.element('.qa-btn-submit-answers')
    submitBtn.waitForExist(10000)
    submitBtn.click()
    const url = browser.url().value
    expect(url).to.contain('thank-you')
  })
})
