import assert from 'assert'
import chai from 'chai'
import {getRandomString, startQuestionnaire} from '../helpers'
import reportingPeriod from '../pages/surveys/rsi/0102/reporting-period.page'
import retailTurnoverPage from '../pages/surveys/rsi/0102/retail-turnover.page'
import internetSalesPage from '../pages/surveys/rsi/0102/internet-sales.page'
import changeInRetailTurnover from '../pages/surveys/rsi/0102/changes-in-retail-turnover.page'
import rsiSummaryPage from '../pages/surveys/rsi/0102/rsi-summary.page'
import devPage from '../pages/dev.page'
import landingPage from '../pages/landing.page'
import multipleSurveys from '../pages/multiple-survey.page'

const expect = chai.expect

describe('RSI - Multiple months of one form type being worked on at the same time ', function() {

    it('Given the RSI survey 0102 when a second surveys is open for a different month then the first survey shows the multiple survey page and the 2nd survey continues to work and has the correct data', function() {

        //Given that RSI business survey 0102
        var user_id = getRandomString(10)
        var collection_id = getRandomString(10)

        devPage.open()
          .setUserId(user_id)
          .setCollectionId('A' + collection_id)
          .setSchema('1_0102.json')
          .setPeriodId('201611')
          .setPeriodString('November2016')
        devPage.submit()

        landingPage.getStarted()

        reportingPeriod.setFromReportingPeriodDay(1)
          .setToReportingPeriodDay(1)
          .setFromReportingPeriodMonth(1)
          .setToReportingPeriodMonth(1)
          .setFromReportingPeriodYear(2016)
          .setToReportingPeriodYear(2017)

        //When a second surveys is open for a different month
        browser.newWindow('/dev', 'second_survey')

        devPage.open()
          .setUserId(user_id)
          .setCollectionId('B' + collection_id)
          .setSchema('1_0102.json')
          .setPeriodId('201610')
          .setPeriodString('October2016')
        devPage.submit()

        landingPage.getStarted()

        reportingPeriod.setFromReportingPeriodDay(2)
          .setToReportingPeriodDay(2)
          .setFromReportingPeriodMonth(1)
          .setToReportingPeriodMonth(1)
          .setFromReportingPeriodYear(2018)
          .setToReportingPeriodYear(2019)
          .submit()

        //Then the 1st survey shows the multiple survey page and the 2nd survey continues to works and has the correct data
        browser.switchTab()
        reportingPeriod.submit()
        expect(multipleSurveys.isOpen()).to.be.true

        browser.switchTab('second_survey')

        retailTurnoverPage.setRetailTurnover(12345)
        retailTurnoverPage.submit()
        internetSalesPage.setInternetSales(1234)
            .submit()
        changeInRetailTurnover.setChangesInRetailTurnover('Test comment')
            .submit()

        expect(rsiSummaryPage.getReportingPeriodSummary()).to.contain('02 January 2018 to 02 January 2019')
        expect(rsiSummaryPage.getRetailTurnoverSummary()).to.contain('£12,345')
        expect(rsiSummaryPage.getInternetSalesSummary()).to.contain('£1,234')
        expect(rsiSummaryPage.getChangeInRetailTurnoverSummary()).to.contain('Test comment')
    })
})
