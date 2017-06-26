import {getRandomString, openQuestionnaire, startQuestionnaire} from '../helpers'
import landingPage from '../pages/landing.page'
import Introduction from '../pages/surveys/rsi/introduction.page.js'
import ReportingPeriod from '../pages/surveys/rsi/reporting-period.page.js'
import TotalRetailTurnoverBlock from '../pages/surveys/rsi/total-retail-turnover-block.page.js'
import TotalInternetSales from '../pages/surveys/rsi/total-internet-sales.page.js'
import SignificantChange from '../pages/surveys/rsi/significant-change.page.js'
import ReasonForChange from '../pages/surveys/rsi/reason-for-change.page.js'
import ChangeCommentBlock from '../pages/surveys/rsi/change-comment-block.page.js'
import TotalEmployees from '../pages/surveys/rsi/total-employees.page.js'
import EmployeesBreakdown from '../pages/surveys/rsi/employees-breakdown.page.js'
import ChangesInEmployeesPage from '../pages/surveys/rsi/changes-in-employees.page'
import Summary from '../pages/surveys/rsi/summary.page.js'
import thankYou from '../pages/thank-you.page'

describe('RSI 0112 Test', function() {

  it('Given the rsi business survey 0112 is selected when I start the survey then the landing page is displayed', function() {
    // Given
    // When
    openQuestionnaire('1_0112refresh.json', getRandomString(10), getRandomString(5))

    // Then
    expect(landingPage.isOpen(), 'Landing page should be open').to.be.true
  })

  it('Given the rsi business survey 0112 has been started when I complete the survey then I reach the thank you page', function() {
    // Given
    startQuestionnaire('1_0112refresh.json', getRandomString(10), getRandomString(5))

    // When
    ReportingPeriod.setPeriodFromDay('01')
        .setPeriodFromMonth(5)
        .setPeriodFromYear('2016')
        .setPeriodToDay('31')
        .setPeriodToMonth(5)
        .setPeriodToYear('2016')
        .submit()

    TotalRetailTurnoverBlock.setTotalRetailTurnover('1234')
        .submit()

    TotalInternetSales.setInternetSales('567')
        .submit()

    SignificantChange.clickSignificantChangeEstablishedAnswerYes()
        .submit()

    ReasonForChange.clickReasonForChangeAnswerWeather()
        .submit()

    ChangeCommentBlock.setChangeComment('Bad weather reduced shop footfall')
        .submit()

    TotalEmployees.setTotalNumberEmployees('100')
        .submit()

    EmployeesBreakdown.setNumberMaleEmployeesOver30Hours('10')
        .setNumberMaleEmployeesUnder30Hours('20')
        .setNumberFemaleEmployeesOver30Hours('30')
        .setNumberFemaleEmployeesUnder30Hours('40')
        .submit()

    ChangesInEmployeesPage.setChangesInEmployeesPage('No reason')
      .submit()

    Summary.submit()

    // Then
    expect(thankYou.isOpen(), 'Thank you page should be open').to.be.true
  })

  it('Given the rsi business survey 0112 has been started and sales questions completed when I select No for significant changes I skip to total employees question', function() {
    // Given
    startQuestionnaire('1_0112refresh.json', getRandomString(10), getRandomString(5))

    ReportingPeriod.setPeriodFromDay('01')
        .setPeriodFromMonth(5)
        .setPeriodFromYear('2016')
        .setPeriodToDay('31')
        .setPeriodToMonth(5)
        .setPeriodToYear('2016')
        .submit()

    TotalRetailTurnoverBlock.setTotalRetailTurnover('0')
        .submit()
    TotalInternetSales.setInternetSales('567')
        .submit()

    // When
    SignificantChange.clickSignificantChangeEstablishedAnswerNo()
        .submit()

    // Then
    expect(TotalEmployees.isOpen(), 'Total Employees page should be open').to.be.true
  })

  it('Given a rsi business survey 0112 previously had errors when I correct the errors then I can submit them', function() {
    // Given
    const userId = getRandomString(10)
    const collectionId = getRandomString(5)
    startQuestionnaire('1_0112refresh.json', userId, collectionId)
    ReportingPeriod.setPeriodFromDay('01')
        .setPeriodFromMonth(5)
        .setPeriodFromYear('2016')
        .setPeriodToDay('01')
        .setPeriodToMonth(5)
        .setPeriodToYear('2016')
        .submit()

    // When
    openQuestionnaire('1_0112refresh.json', userId, collectionId)

    ReportingPeriod.setPeriodFromDay('01')
        .setPeriodFromMonth(5)
        .setPeriodFromYear('2016')
        .setPeriodToDay('01')
        .setPeriodToMonth(5)
        .setPeriodToYear('2017')
        .submit()

    TotalRetailTurnoverBlock.setTotalRetailTurnover('12345')
        .submit()

    TotalInternetSales.setInternetSales('567')
        .submit()

    SignificantChange.clickSignificantChangeEstablishedAnswerNo()
        .submit()

    TotalEmployees.setTotalNumberEmployees('6')
        .submit()

    EmployeesBreakdown.submit()

    ChangesInEmployeesPage.submit()

    Summary.submit()

    // Then
    expect(thankYou.isOpen(), 'Thank you page should be open').to.be.true
  })
})
