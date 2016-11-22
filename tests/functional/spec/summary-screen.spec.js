import assert from 'assert'
import chai from 'chai'
import {getRandomString, startQuestionnaire} from '../helpers'
import reportingPeriod from '../pages/surveys/rsi/0102/reporting-period.page'
import retailTurnoverPage from '../pages/surveys/rsi/0102/retail-turnover.page'
import internetSalesPage from '../pages/surveys/rsi/0102/internet-sales.page'
import changeInRetailTurnover from '../pages/surveys/rsi/0102/changes-in-retail-turnover.page'
import rsiSummaryPage from '../pages/surveys/rsi/0102/rsi-summary.page'
import SummaryPage from '../pages/summary.page'

const expect = chai.expect

describe('RSI - summary screen edit test', function() {

  it('Given the RSI business survey 0102 is started when data is entered for the survey then summary screen shows the data entered', function(done) {

    //Given the RSI business survey 0102 is started
    startQuestionnaire('1_0102.json')

    // when data is entered for the survey
    reportingPeriod.setFromReportingPeriodDay(2)
      .setToReportingPeriodDay(2)
      .setFromReportingPeriodMonth(5)
      .setToReportingPeriodMonth(5)
      .setFromReportingPeriodYear(2016)
      .setToReportingPeriodYear(2017)
      .submit()
    retailTurnoverPage.setRetailTurnover(12345)
      .submit()
    internetSalesPage.setInternetSales(1234)
      .submit()
    changeInRetailTurnover.setChangesInRetailTurnover('This is to test edit links on summary screen')
      .submit()

    // Then summary screen shows the data entered
    expect(rsiSummaryPage.getReportingPeriodSummary()).to.contain('02 May 2016 to 02 May 2017')
    expect(rsiSummaryPage.getRetailTurnoverSummary()).to.contain('£12,345')
    expect(rsiSummaryPage.getInternetSalesSummary()).to.contain('£1,234')
    expect(rsiSummaryPage.getChangeInRetailTurnoverSummary()).to.contain('This is to test edit links on summary screen')
  })

  it('Given the RSI survery 0102 is saved with answers when edit link is clicked then it should allow to edit the answer ', function(done) {

    //Given the RSI survery 0102 is saved with answers
    startQuestionnaire('1_0102.json')
    reportingPeriod.setFromReportingPeriodDay(2)
      .setToReportingPeriodDay(2)
      .setFromReportingPeriodMonth(5)
      .setToReportingPeriodMonth(5)
      .setFromReportingPeriodYear(2016)
      .setToReportingPeriodYear(2017)
      .submit()
    retailTurnoverPage.setRetailTurnover(12345)
      .submit()
    internetSalesPage.setInternetSales(1234)
      .submit()
    changeInRetailTurnover.setChangesInRetailTurnover('This is to test edit links on summary screen')
      .submit()

    // When edit link is clicked
    rsiSummaryPage.editLinkChangeInRetailTurnover()

    //Then it should allow to edit the answer
    expect(changeInRetailTurnover.getQuestionTextChangeInRetailTurnover()).to.contain('Changes in total retail turnover')
    changeInRetailTurnover.setChangesInRetailTurnover('This is to test edit links on summary screen - edited')
      .submit()
    expect(rsiSummaryPage.getChangeInRetailTurnoverSummary()).to.contain('This is to test edit links on summary screen - edited')

  })
  it('Given the RSI survery 0102 when a 0 is entered in a currency field then the summary screen should show £0 and the original page should show 0', function(done) {

    //Given the RSI business survey 0102 is started
    startQuestionnaire('1_0102.json')

    // when data is entered for the survey
    reportingPeriod.setFromReportingPeriodDay(2)
      .setToReportingPeriodDay(2)
      .setFromReportingPeriodMonth(5)
      .setToReportingPeriodMonth(5)
      .setFromReportingPeriodYear(2016)
      .setToReportingPeriodYear(2017)
      .submit()
    retailTurnoverPage.setRetailTurnover(1000)
      .submit()
    internetSalesPage.setInternetSales(0)
      .submit()
    changeInRetailTurnover.setChangesInRetailTurnover('')
      .submit()

    // Then summary screen and the original page shows the data entered
    expect(rsiSummaryPage.getRetailTurnoverSummary()).to.contain('£1,000')
    expect(rsiSummaryPage.getInternetSalesSummary()).to.contain('£' + 0)
    rsiSummaryPage.editLinkChangeInternetSales()
    expect(internetSalesPage.getInternetSales()).to.contain('0')

  })
})
