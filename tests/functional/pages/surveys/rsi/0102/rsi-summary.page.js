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

  editLinkChangeInRetailTurnover(){
    browser.click('[aria-describedby="summary-3-0-0 summary-3-0-0-answer"]')
  }

  editLinkChangeInternetSales(){
    browser.click('[aria-describedby="summary-2-0-0 summary-2-0-0-answer"]')
  }

}

export default new RSISummaryPage()
