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
    browser.setValue(userId, 'yoganandkunche')
    browser.waitForExist(collectionSID)
    browser.setValue(collectionSID, '7890102')
    browser.waitForExist(selectSchema)
    browser.selectByValue(selectSchema, '1_0102.json')
    browser.click('.qa-btn-submit-dev')
  })

  it('The landing page has been reached for 0102', function(done) {
    const getStartedBtn = browser.element('.qa-btn-get-started')
    getStartedBtn.waitForExist(10000)
    const url = browser.url().value
    expect(url).to.contain('introduction')
    getStartedBtn.click()
  })

  it('The questionnaire page for 0102 has been reached', function(done) {
    const questionnaireElementExists = browser.isExisting('.qa-questionnaire-form')
    expect(questionnaireElementExists).to.equal(true)
  })

  it('Enter Data in to 0102 questionnaire', function(done) {
    const questionnaireElementExists = browser.isExisting('.qa-questionnaire-form')
    expect(questionnaireElementExists).to.equal(true)
    const submitBtn = browser.element('.qa-btn-submit')
    submitBtn.waitForExist(10000)
    browser.setValue('[id = "94f368e4-7c6c-4272-a780-8c46328626a2-year"]', '2016')
    browser.setValue('#dc156715-3d48-4af3-afed-7a0a6bb65583-year', '2016')
    const saveandcontinueBtn2 = browser.element('.qa-btn-submit')
    saveandcontinueBtn2.click();
    const erroralert = browser.element('.alert__body')
    const Q1text = erroralert.getText()
    const experror = 'The \'to\' date must be different to the \'from\' date.'
    if(Q1text.indexOf(experror) > -1) {
      console.log('Expected Text is present: ' + experror );
    } else {
      console.log(Q1text.indexOf(experror) !== -1);
      assert.equal(Q1text, experror);
    }
  })

  it('Progress from the developer page for 1_0112', function() {
    const userId = '.qa-user-id'
    const collectionSID = '.qa-collection-sid'
    const selectSchema = '.qa-select-schema'
    browser.url('/dev')
    browser.waitForExist(userId)
    browser.setValue(userId, 'yoganandkunche')
    browser.waitForExist(collectionSID)
    browser.setValue(collectionSID, '7890112')
    browser.waitForExist(selectSchema)
    browser.selectByValue(selectSchema, '1_0112.json')
    browser.click('.qa-btn-submit-dev')
  })

  it('The landing page has been reached for 0112', function(done) {
    const getStartedBtn = browser.element('.qa-btn-get-started')
    getStartedBtn.waitForExist(10000)
    const url = browser.url().value
    expect(url).to.contain('introduction')
    getStartedBtn.click()
  })

  it('The questionnaire page for 0112 has been reached', function(done) {
    const questionnaireElementExists = browser.isExisting('.qa-questionnaire-form')
    expect(questionnaireElementExists).to.equal(true)
  })

  it('Enter Data in to 0112 questionnaire', function(done) {
    const questionnaireElementExists = browser.isExisting('.qa-questionnaire-form')
    expect(questionnaireElementExists).to.equal(true)
    const submitBtn = browser.element('.qa-btn-submit')
    submitBtn.waitForExist(10000)
    browser.setValue('#fad63234-1083-4f6a-826a-20b5df6e4baa-year', '2016')
    browser.setValue('#c8c4bd92-fd45-4fd1-83b6-18c813de2df2-year', '2017')
    const saveandcontinueBtn2 = browser.element('.qa-btn-submit')
    saveandcontinueBtn2.click();
    submitBtn.waitForExist(10000)
    browser.setValue('.input--currency', 'Test')
    const saveandcontinueBtn3 = browser.element('.qa-btn-submit')
    saveandcontinueBtn3.click();
    const erroralert2 = browser.element('.alert__body')
    const Q2text = erroralert2.getText()
    const experror2 = 'Please only enter whole numbers into the field.'
    if(Q2text.indexOf(experror2) > -1) {
      console.log('Expected Text is present: ' + experror2 );
    } else {
      console.log(Q2text.indexOf(experror2) !== -1);
      assert.equal(Q2text, experror2);
    }
  })
  // Revisiting 0102
  it('Progress from the developer page for 1_0102', function() {
    const userId = '.qa-user-id'
    const collectionSID = '.qa-collection-sid'
    const selectSchema = '.qa-select-schema'
    browser.url('/dev')
    browser.waitForExist(userId)
    browser.setValue(userId, 'yoganandkunche')
    browser.waitForExist(collectionSID)
    browser.setValue(collectionSID, '7890102')
    browser.waitForExist(selectSchema)
    browser.selectByValue(selectSchema, '1_0102.json')
    browser.click('.qa-btn-submit-dev')
  })

  it('To make sure the error page has been reached for 0102 revisit', function(done) {
    const saveandcontinueBtn4 = browser.element('.qa-btn-submit')
    saveandcontinueBtn4.waitForExist(10000)
    const erroralert = browser.element('.alert__body')
    const Q1text = erroralert.getText()
    const experror = 'The \'to\' date must be different to the \'from\' date.'
    if(Q1text.indexOf(experror) > -1) {
      console.log('Expected Text is present: ' + experror );
    } else {
      console.log(Q1text.indexOf(experror) !== -1);
      assert.equal(Q1text, experror);
    }
  })

  it('Correcting the error and submitting the 0102 form', function(done) {
    const questionnaireElementExists = browser.isExisting('.qa-questionnaire-form')
    expect(questionnaireElementExists).to.equal(true)
    const submitBtn = browser.element('.qa-btn-submit')
    submitBtn.waitForExist(10000)
    browser.setValue('[id = "94f368e4-7c6c-4272-a780-8c46328626a2-year"]', '2016')
    browser.setValue('#dc156715-3d48-4af3-afed-7a0a6bb65583-year', '2017')
    const saveandcontinueBtn2 = browser.element('.qa-btn-submit')
    saveandcontinueBtn2.click();
    browser.setValue('.input--currency', '12345')
    const saveandcontinueBtn3 = browser.element('.qa-btn-submit')
    saveandcontinueBtn3.click();
    browser.setValue('.input--currency', '1234')
    const saveandcontinueBtn4 = browser.element('.qa-btn-submit')
    saveandcontinueBtn4.click();
    browser.setValue('.input--textarea', 'This is for RSI 0102 Save and restore testing')
    const saveandcontinueBtn5 = browser.element('.qa-btn-submit')
    saveandcontinueBtn5.click();
  })
  it('The survey can be completed with "thankyou page" reached', function(done) {
    const finalsubmitBtn = browser.element('.qa-btn-submit-answers')
    finalsubmitBtn.waitForExist(10000)
    finalsubmitBtn.click();
    const url = browser.url().value
    expect(url).to.contain('thank-you')
  })

  // Revisiting 0112
  it('Progress from the developer page for 1_0112', function() {
    const userId = '.qa-user-id'
    const collectionSID = '.qa-collection-sid'
    const selectSchema = '.qa-select-schema'
    browser.url('/dev')
    browser.waitForExist(userId)
    browser.setValue(userId, 'yoganandkunche')
    browser.waitForExist(collectionSID)
    browser.setValue(collectionSID, '7890112')
    browser.waitForExist(selectSchema)
    browser.selectByValue(selectSchema, '1_0112.json')
    browser.click('.qa-btn-submit-dev')
  })
  it('To make sure the error page has been reached for 0112 on revisit', function(done) {
    const saveandcontinueBtn4 = browser.element('.qa-btn-submit')
    saveandcontinueBtn4.waitForExist(10000)
    const erroralert = browser.element('.alert__body')
    const Q2text = erroralert.getText()
    const experror2 = 'Please only enter whole numbers into the field.'
    if(Q2text.indexOf(experror2) > -1) {
      console.log('Expected Text is present: ' + experror2 );
    } else {
      console.log(Q2text.indexOf(experror2) !== -1);
      assert.equal(Q2text, experror2);
    }
  })

  it('Correcting the error and submitting the 0112 form', function(done) {
    const questionnaireElementExists = browser.isExisting('.qa-questionnaire-form')
    expect(questionnaireElementExists).to.equal(true)
    const submitBtn = browser.element('.qa-btn-submit')
    submitBtn.waitForExist(10000)
    browser.setValue('.input--currency', '12345')
    browser.element('.qa-btn-submit').click();
    browser.setValue('.input--currency', '1234')
    browser.element('.qa-btn-submit').click();
    browser.setValue('.input--textarea', 'This is for RSI 0112 Save and restore testing')
    browser.element('.qa-btn-submit').click();
    browser.setValue('[name = "c6881970-98ff-4005-af4a-60bfd9b6179f"]', '13')
    browser.element('.qa-btn-submit').click();
    browser.setValue('.input--textarea', 'Changes in employee figures')
    browser.element('.qa-btn-submit').click();
  })

  it('The survey can be completed with "thankyou page" reached', function(done) {
    const finalsubmitBtn = browser.element('.qa-btn-submit-answers')
    finalsubmitBtn.waitForExist(10000)
    finalsubmitBtn.click();
    const url = browser.url().value
    expect(url).to.contain('thank-you')
  })
})
