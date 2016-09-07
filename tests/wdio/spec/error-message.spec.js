import chai from 'chai'
import {getRandomString} from '../helpers'

const expect = chai.expect

describe('Error messages', function() {
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
    browser.selectByValue(selectSchema, '0_basetheme.json')
    browser.click('.qa-btn-submit-dev')
  })

  it('The landing page has been reached', function(done) {
    const getStartedBtn = browser.element('.qa-btn-get-started')
    getStartedBtn.waitForExist(10000)
    const url = browser.url().value
    expect(url).to.contain('introduction')
    getStartedBtn.click()
    browser.call(done)
  })

  it('The questionnaire page has been reached', function(done) {
    const questionnaireElementExists = browser.isExisting('.qa-questionnaire-form')
    expect(questionnaireElementExists).to.equal(true)
    browser.call(done)
  })

  it('The form can be filled in and submitted to return error', function(done) {
    const submitBtn = browser.element('.qa-btn-submit')
    submitBtn.waitForExist(10000)
    browser.setValue('[id="94f368e4-7c6c-4272-a780-8c46328626a2-year"]', '')
    browser.setValue('[id="dc156715-3d48-4af3-afed-7a0a6bb65583-year"]', '')
    submitBtn.click()
    const url = browser.url().value
    expect(url).to.contain('5bce8d8f-0af8-4d35-b77d-744e6179b406')
    browser.call(done)
  })

  it('Error link is clicked to take focus to day input', function(done) {
    const inPageLink = browser.element('.js-inpagelink-trigger')
    inPageLink.waitForExist(10000)
    inPageLink.click()
    browser.timeoutsImplicitWait(10000)
    const activeElementValueNumber = browser.elementActive().value.ELEMENT
    const activeElementValue = browser.elementIdAttribute(activeElementValueNumber, "id").value
    expect(activeElementValue).to.contain('94f368e4-7c6c-4272-a780-8c46328626a2-day')
    browser.call(done)
  })

})
