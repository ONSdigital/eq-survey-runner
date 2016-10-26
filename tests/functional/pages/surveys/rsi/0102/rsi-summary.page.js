import SummaryPage from '../../../summary.page'

class RSISummaryPage extends SummaryPage {

  getReportingPeriodSummary() {
    return browser.element('[data-qa="94f368e4-7c6c-4272-a780-8c46328626a2-answer"]').getText()
  }

  getRetailTurnoverSummary() {
    return browser.element('[data-qa="ea08f977-33a8-4933-ad7b-c497997107cf-answer"]').getText()
  }

  getInternetSalesSummary() {
    return browser.element('[data-qa="66612bbb-bc06-4d38-b32c-e2a113641c8a-answer"]').getText()
  }

  getChangeInRetailTurnoverSummary() {
    return browser.element('[data-qa="568e2c81-b11d-4682-bd89-f170481c9a48-answer"]').getText()
  }

  editLinkChangeInRetailTurnover(){
    browser.click('[data-qa="568e2c81-b11d-4682-bd89-f170481c9a48-edit"]')
  }

  editLinkChangeInternetSales(){
    browser.click('[data-qa="66612bbb-bc06-4d38-b32c-e2a113641c8a-edit"]')
  }

}

export default new RSISummaryPage()
