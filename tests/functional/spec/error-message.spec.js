import chai from 'chai'
import {startQuestionnaire, getElementId} from '../helpers'
import monthlyBusinessSurveyPage from '../pages/surveys/mci/monthly-business-survey.page'

const expect = chai.expect

describe('Error messages', function() {

  it('Given the monthly business survey contains errors when the error link is clicked then the day input field is focused', function() {
    // Given
    startQuestionnaire('1_0205.json')
    monthlyBusinessSurveyPage.setFromReportingPeriodDay('01')
      .setFromReportingPeriodYear('2016')
      .setToReportingPeriodDay('01')
      .setToReportingPeriodYear('2016')
      .submit()

    // When
    monthlyBusinessSurveyPage.focusErrorField()

    // Then
    expect(getElementId(browser.elementActive())).to.equal(getElementId(monthlyBusinessSurveyPage.getFromReportingPeriodDay()))
  })
})
