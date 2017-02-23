import assert from 'assert'
import {getRandomString, startQuestionnaire, openQuestionnaire} from '../helpers'
import devPage from '../pages/dev.page'
import landingPage from '../pages/landing.page'
import thankYou from '../pages/thank-you.page'
import signOut from '../pages/sign-out.page'
import reportingPeriod from '../pages/surveys/rsi/0102/reporting-period.page'
import retailTurnoverPage from '../pages/surveys/rsi/0102/retail-turnover.page'
import internetSalesPage from '../pages/surveys/rsi/0102/internet-sales.page'
import changeInRetailTurnover from '../pages/surveys/rsi/0102/changes-in-retail-turnover.page'
import SummaryPage from '../pages/summary.page'


describe('RSI - Save and restore test', function() {

  it('Given I am completing survey 0102, when I select save and complete later, then I am redirected to sign out page and my session is cleared', function() {

    // Given I am completing survey 0102
    const collectionId = getRandomString(5)
    startQuestionnaire('1_0102.json', 'test_user', collectionId)
    const url = browser.getUrl();
    reportingPeriod.setFromReportingPeriodDay('01')
      .setFromReportingPeriodMonth(5)
      .setFromReportingPeriodYear('2016')
      .setToReportingPeriodDay('01')
      .setToReportingPeriodMonth(5)
      .setToReportingPeriodYear('2017')
      .submit()

    // When I select save and complete later
    retailTurnoverPage.saveSignOut()

    // Then I am redirected to sign out page and my session is cleared
    expect(signOut.isOpen(), 'sign out page should be open').to.be.true
    browser.url(url)
    expect(browser.getSource()).to.contain('Your session has expired')
    })


  it('Given whilst completing survey 0102 I have opted to save and complete later, when I return to the questionnaire, then I am returned to the page I was on and can then complete the survey', function() {

    // Given whilst completing survey 0102 I have opted to save and complete later
    const collectionId = getRandomString(5)
    startQuestionnaire('1_0102.json', 'test_user', collectionId)
    reportingPeriod.setFromReportingPeriodDay('01')
      .setFromReportingPeriodMonth(5)
      .setFromReportingPeriodYear('2016')
      .setToReportingPeriodDay('01')
      .setToReportingPeriodMonth(5)
      .setToReportingPeriodYear('2017')
      .submit()
    retailTurnoverPage.saveSignOut()
    expect(signOut.isOpen(), 'sign out page should be open').to.be.true

    // When I return to the questionnaire
    openQuestionnaire('1_0102.json', 'test_user', collectionId)

    // Then I am returned to the page I was on and can then complete the survey
    expect(retailTurnoverPage.isOpen(), 'retail turnover page should be open').to.be.true
    expect(retailTurnoverPage.getRetailTurnover()).to.contain('')
    retailTurnoverPage.setRetailTurnover('3000')
      .submit()
    internetSalesPage.setInternetSales('2000')
      .submit()
    changeInRetailTurnover.setChangesInRetailTurnover('No reason')
      .submit()
    SummaryPage.submit()
    expect(thankYou.isOpen(), 'Thank you page should be open').to.be.true
    })

  })
