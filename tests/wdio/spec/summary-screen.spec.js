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
  })

  it('Verify data on summary screen', function(done) {
    const submitAnswers = browser.isExisting('.qa-btn-submit-answers')
    expect(submitAnswers).to.equal(true)

    const Q1text = browser.element('[data-qa="answer-0-0 answer-type-date"]').getText()
    const q1expText = '01 Jan 2016 to 01 Jan 2017'
    if(Q1text.indexOf(q1expText) > -1) {
      console.log('Expected Data is present: ' + q1expText );
    } else {
      console.log(Q1text.indexOf(q1expText) !== -1);
      assert.equal(Q1text, q1expText);
    }
    const Q2text = browser.element('[data-qa="answer-1-0 answer-type-currency"]').getText()
    const q2expText = '£12,345'
    if(Q2text.indexOf(q2expText) > -1) {
      console.log('Expected Data is present: ' + q2expText );
    } else {
      console.log(Q3text.indexOf(q2expText) !== -1);
      assert.equal(Q2text, q2expText);
    }
    const Q3text = browser.element('[data-qa="answer-2-0 answer-type-currency"]').getText()
    const q3expText = '£1,234'
    if(Q3text.indexOf(q3expText) > -1) {
      console.log('Expected Data is present: ' + q3expText );
    } else {
      console.log(Q3text.indexOf(q3expText) !== -1);
      assert.equal(Q3text, q3expText);
    }

    const Q4text = browser.element('[data-qa="answer-3-0 answer-type-textarea"]').getText()
    const q4expText = 'This is to test edit links on summary screen'
    if(Q4text.indexOf(q4expText) > -1) {
      console.log('Expected Data is present: ' + q4expText );
    } else {
      console.log(Q4text.indexOf(q4expText) !== -1);
      assert.equal(Q4text, q4expText);
    }
  })
  it('Tests Edit link on the summary screen', function(done) {

    browser.element('[aria-describedby="summary-3-0 summary-3-0-answer"]').click();
    const submitBtn = browser.element('.qa-btn-submit')
    submitBtn.waitForExist(10000)
    const qHeading = browser.element('.section__title').getText()
    const expectedQHeading = 'Changes in total retail turnover'
    assert.equal(qHeading,expectedQHeading)
    browser.setValue('.input--textarea', 'This is to test edit links on summary screen - edited')
    browser.element('.qa-btn-submit').click();

    const Q4text = browser.element('[data-qa="answer-3-0 answer-type-textarea"]').getText()
    //  console.log('Text in Q4 field: ' + Q4text );
    const q4expText = 'This is to test edit links on summary screen - edited'
    if(Q4text.indexOf(q4expText) > -1) {
      console.log('Expected Data is present: ' + q4expText );
    } else {
      console.log(Q4text.indexOf(q4expText) !== -1);
      assert.equal(Q4text, q4expText);
    }

  })
})
