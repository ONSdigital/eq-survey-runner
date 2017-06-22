import {startQuestionnaire, getElementId} from '../helpers'
import ReportingPeriod from '../pages/surveys/mci/reporting-period.page.js'


describe('Error messages', function() {

  it('Given the monthly business survey contains errors when the error link is clicked then the day input field is focused', function() {
    // Given
    startQuestionnaire('1_0215.json')


    ReportingPeriod.setPeriodFromDay('01')
      .setPeriodFromYear('2016')
      .setPeriodToDay('31')
      .setPeriodToMonth(5)
      .setPeriodToYear('2016')
      .submit()

    // When
    ReportingPeriod.focusErrorField()

    // Then
    expect(getElementId(browser.elementActive())).to.equal(getElementId(ReportingPeriod.getPeriodFromDayId()))
  })
})
