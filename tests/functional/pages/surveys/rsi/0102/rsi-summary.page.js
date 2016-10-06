import SummaryPage from '../../../summary.page'

class RSISummaryPage extends SummaryPage {

  getReportingPeriodSummary() {
    return browser.element('[data-qa="answer-0-0 answer-type-date"]').getText()
  }

  getRetailTurnoverSummary() {
    return browser.element('[data-qa="answer-1-0 answer-type-currency"]').getText()
  }

  getInternetSalesSummary() {
    return browser.element('[data-qa="answer-2-0 answer-type-currency"]').getText()
  }

  getChangeInRetailTurnoverSummary() {
    return browser.element('[data-qa="answer-3-0 answer-type-textarea"]').getText()
  }

}

export default new RSISummaryPage()
