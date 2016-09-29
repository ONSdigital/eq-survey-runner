import chai from 'chai'
import {getRandomString} from '../helpers'

import devPage from '../pages/dev.page'
import landingPage from '../pages/landing.page'
import summaryPage from '../pages/summary.page'
import thankYou from '../pages/thank-you.page'
import monthlyBusinessSurveyPage from '../pages/surveys/monthly-business-survey.page'

const expect = chai.expect

describe('MCI test', function() {

  before('Progress from the developer page', function() {
    devPage.open()
      .setUserId(getRandomString(10))
      .setCollectionId(getRandomString(3))
      .setSchema('1_0205.json')
      .submit()
  })

  it('The landing page has been reached', function(done) {
    expect(landingPage.isOpen()).to.be.true
  })

  it('The questionnaire page has been reached', function(done) {
    landingPage.getStarted()
    expect(monthlyBusinessSurveyPage.isOpen(), 'Survey page should be open').to.be.true
  })

  it('The form can be filled in and submitted', function(done) {
    monthlyBusinessSurveyPage.setFromSalesPeriodDay('01')
      .setFromSalesPeriodYear('2016')
      .setToSalesPeriodDay('01')
      .setToSalesPeriodYear('2017')
      .setRetailBusinessTurnover(2000)
      .submit()
  })

  it('The summary is displayed after questionnaire is submitted', function(done) {
    expect(summaryPage.isOpen(), 'Summary page should be open').to.be.true
    summaryPage.submit()
  })

  it('The thank you page is displayed after submitting', function(done) {
    expect(thankYou.isOpen(), 'Thank you page should be open').to.be.true
  })

})
