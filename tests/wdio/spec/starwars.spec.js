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
    browser.selectByValue(selectSchema, '0_star_wars.json')
    browser.click('.qa-btn-submit-dev')
  })
  function logTitle() {
    browser.getTitle().then(function(title)){
    console.log('Current Page Title: ' +title)
    });
    }
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

  it('Enter Data in to questionnaire', function(done) {
    const questionnaireElementExists = browser.isExisting('.qa-questionnaire-form')
    expect(questionnaireElementExists).to.equal(true)
    var selectbox = browser.element('ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c-2')
    selectbox.selectByValue('ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c-2')
    console.log(selectbox.getValue());
    const saveandcontinue = browser.element('')
    saveandcontinue.click();
    const secondquestion = browser.isExisting('d9fd4a58-83a5-44df-a413-47ce41244124')
    console.log(secondquestion.getValue());
    browser.call(done)
  })
})
