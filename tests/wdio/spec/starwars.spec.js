import chai from 'chai'
import {getRandomString} from '../helpers'

const expect = chai.expect

describe('StarWars Routing', function() {
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

  it ('get Title', function (done) {
    const title= browser.getTitle()
    console.log('Current Page Title: ' +title)
    // browser.debug()
    browser.call(done)
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

  it('Enter Data in to questionnaire', function(done) {
    const questionnaireElementExists = browser.isExisting('.qa-questionnaire-form')
    expect(questionnaireElementExists).to.equal(true)
    browser.click('#ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c-1')
  //  browser.debug()
    const saveandcontinueBtn = browser.element('.qa-btn-submit')
    saveandcontinueBtn.click();
    const Q1text = browser.getText('[id = main]')
    expect(Q1text).to.have.string('A wise choice young Yedi. Pick your hero')
    console.log('Routing Sucessful after question 1 Sucessful')

    browser.click('#label-91631df0-4356-4e9f-a9d9-ce8b08d26eb3-1')
    browser.click('#label-2e0989b8-5185-4ba6-b73f-c126e3a06ba7-2')

    const saveandcontinueBtn2 = browser.element('.qa-btn-submit')
    saveandcontinueBtn2.click();

    const Q2text = browser.getText('[id = main]')
    expect(Q2text).to.have.string('How many starting crawlers do you know?')
    console.log('Routing Sucessful after question 2 Sucessful')

    var input = browser.element('.input--text');
    input.setValue('1')

    const saveandcontinueBtn3 = browser.element('.qa-btn-submit')
    saveandcontinueBtn3.click()

    const saveandcontinueBtn4 = browser.element('.qa-btn-submit')
    saveandcontinueBtn4.waitForExist(10000)

    var input_Crawler = browser.element('.input--textarea')
    input_Crawler.setValue('Is a very nice one')


    saveandcontinueBtn4.click()

    //    const saveandcontinueBtn5 = browser.element('.qa-btn-submit')
    //    saveandcontinueBtn5.waitForExist(10000)
    //  const noofcrawlers = '.input--text'
    //   browser.setValue(noofcrawlers, '1')
    //const secondquestion = browser.isExisting('d9fd4a58-83a5-44df-a413-47ce41244124')

    browser.debug()
    browser.call(done)
  })
})
