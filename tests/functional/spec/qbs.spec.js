import chai from 'chai'
import {startQuestionnaire} from '../helpers'

import thankYou from '../pages/thank-you.page'
import SummaryPage from '../pages/summary.page'
import NumberOfEmployeesPage from '../pages/surveys/qbs/number-of-employees.page.js'

const expect = chai.expect

describe('QBS survey test', function() {

  it('Given a QBS business survey 0001 has been started, when I successfully complete the survey, then I reach the thank you page', function() {
    // Given
    startQuestionnaire('2_0001.json')

    // When
    NumberOfEmployeesPage.setNumberOfEmployeesMaleMore30Hours(1)
      .setNumberOfEmployeesMaleLess30Hours(2)
      .setNumberOfEmployeesFemaleMore30Hours(3)
      .setNumberOfEmployeesFemaleLess30Hours(4)
      .setNumberOfEmployeesTotal(10)
      .submit()

    SummaryPage.submit()

    // Then
    expect(thankYou.isOpen(), 'Thank you page should be open').to.be.true
  })

})
