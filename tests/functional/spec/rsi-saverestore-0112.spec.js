import assert from 'assert'
import chai from 'chai'
import {getRandomString, startQuestionnaire, openQuestionnaire} from '../helpers'
import devPage from '../pages/dev.page'
import landingPage from '../pages/landing.page'
import thankYou from '../pages/thank-you.page'
import reportingPeriod from '../pages/surveys/rsi/0112/reporting-period.page'
import retailTurnoverPage from '../pages/surveys/rsi/0112/retail-turnover.page'
import internetSalesPage from '../pages/surveys/rsi/0112/internet-sales.page'
import changeInRetailTurnover from '../pages/surveys/rsi/0112/changes-in-retail-turnover.page'
import employeesPage from '../pages/surveys/rsi/0112/employees.page'
import changesInEmployeesPage from '../pages/surveys/rsi/0112/changes-in-employees.page'
import SummaryPage from '../pages/summary.page'

const expect = chai.expect

describe('RSI - Save and restore test', function() {

  it('Given the rsi business survey 0112 is selected when I start the survey then the landing page is displayed', function() {
    // Given
    devPage.open()
      .setUserId(getRandomString(10))
      .setCollectionId(getRandomString(3))
      .setSchema('1_0112.json')

    // When
    devPage.submit()

    // Then
    expect(landingPage.isOpen()).to.be.true
  })

  it('Given the rsi business survey 0112 is displayed when invalid currency is reported then an error is displayed', function() {
    // Given
    startQuestionnaire('1_0112.json')

    // When
    reportingPeriod.setFromReportingPeriodDay('01')
      .setFromReportingPeriodYear('2016')
      .setToReportingPeriodDay('01')
      .setToReportingPeriodYear('2017')
      .submit()
    retailTurnoverPage.setRetailTurnover('test')
      .submit()

    // Then
    expect(retailTurnoverPage.getAlertText()).to.contain('Please only enter whole numbers into the field.')
  })

  it('Given a rsi business survey 0112 previously had errors when I correct the errors then I can submit them', function() {
    // Given
    const collectionId = getRandomString(5)
    startQuestionnaire('1_0112.json', 'yoganandkunche', collectionId)
    reportingPeriod.setFromReportingPeriodDay('01')
      .setFromReportingPeriodYear('2016')
      .setToReportingPeriodDay('01')
      .setToReportingPeriodYear('2016')
      .submit()

    // When
    openQuestionnaire('1_0112.json', 'yoganandkunche', collectionId)

    reportingPeriod.setFromReportingPeriodDay('01')
      .setFromReportingPeriodYear('2016')
      .setToReportingPeriodDay('01')
      .setToReportingPeriodYear('2017')
      .submit()
    retailTurnoverPage.setRetailTurnover('2000')
      .submit()
    internetSalesPage.setInternetSales('2000')
      .submit()
    changeInRetailTurnover.setChangesInRetailTurnover('No reason')
      .submit()
    employeesPage.setEmployees(10)
      .submit()
    changesInEmployeesPage.setChangesInEmployeesPage('No reason')
      .submit()

    SummaryPage.submit()

    // Then
    expect(thankYou.isOpen(), 'Thank you page should be open').to.be.true
  })
})
