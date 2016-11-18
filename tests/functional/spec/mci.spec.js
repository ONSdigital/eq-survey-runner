import chai from 'chai'
import {getRandomString, startQuestionnaire} from '../helpers'

import devPage from '../pages/dev.page'
import landingPage from '../pages/landing.page'
import SummaryPage from '../pages/summary.page'
import thankYou from '../pages/thank-you.page'
import monthlyBusinessSurveyPage from '../pages/surveys/mci/monthly-business-survey.page'

const expect = chai.expect

describe('MCI test', function() {

  it('Given the mci business survey 0205 is selected when I start the survey then the landing page is displayed', function() {
    // Given
    devPage.open()
        .setUserId(getRandomString(10))
        .setCollectionId(getRandomString(3))
        .setSchema('1_0205.json')

    // When
    devPage.submit()

    // Then
    expect(landingPage.isOpen(), 'Landing page should be open').to.be.true
  })

  it('Given a mci business survey 0205 has been started when I complete the survey then I reach the thank you page', function() {
    // Given
    startQuestionnaire('1_0205.json')

    // When
    monthlyBusinessSurveyPage.setFromReportingPeriodDay('01')
      .setFromReportingPeriodMonth(1)
      .setFromReportingPeriodYear('2016')
      .setToReportingPeriodDay('01')
      .setToReportingPeriodMonth(1)
      .setToReportingPeriodYear('2017')
      .setRetailBusinessTurnover(2000)
      .submit()
    SummaryPage.submit()

    // Then
    expect(thankYou.isOpen(), 'Thank you page should be open').to.be.true
  })

})
