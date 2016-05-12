import chai from 'chai'
import {getUri, getRandomString} from '../helpers'

const expect = chai.expect

describe('MCI test', function() {
  before('Progress from the developer page', () => {
    const userId = '.qa-user-id'
    const selectSchema = '.qa-select-schema'

    browser
      .url('/dev')
      .waitForExist(userId)
    browser
      .setValue(userId, getRandomString(10))
    browser
      .waitForExist(selectSchema)
    browser
      .selectByValue(selectSchema, '1_0205.json')
      .click('.qa-btn-submit-dev')
  })

  it('The landig page has been reached', function() {
    const url = browser.url().value
    expect(url).to.equal(getUri('/questionnaire/introduction'))
    browser.click('.qa-btn-get-started')
  })

  it('The questionnaire page has been reached', function() {
    const questionnaireElementExists = browser.isExisting('.qa-questionnaire-form')
    expect(questionnaireElementExists).to.equal(true)
  })

  it('The form can be filled in and submitted', function() {
    const submitBtn = '.qa-btn-submit'
    browser.waitForExist(submitBtn)
    browser
      .setValue('#6fd644b0-798e-4a58-a393-a438b32fe637-year', '2016')
      .setValue('#06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year', '2017')
    browser.setValue('.input-type--currency .input', 2000)
    browser.click(submitBtn)
    const url = browser.url().value
    expect(url).to.equal(getUri('/questionnaire/summary'))
  })

  it('The survey can be completed with "thankyou page" reached', function() {
    const submitBtn = '.qa-btn-submit-answers'
    browser.waitForExist(submitBtn)
    browser.click(submitBtn)
    const url = browser.url().value
    expect(url).to.equal(getUri('/questionnaire/thank-you'))
  })
})
