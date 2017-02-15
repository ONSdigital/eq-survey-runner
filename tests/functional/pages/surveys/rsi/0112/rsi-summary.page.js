import SummaryPage from '../../../summary.page'

class RSISummaryPage extends SummaryPage {

  getReportingPeriodSummary() {
    return browser.element('[data-qa="period-from-answer"]').getText()
  }

  getRetailTurnoverSummary() {
    return browser.element('[data-qa="total-retail-turnover-answer-answer"]').getText()
  }

  getInternetSalesSummary() {
    return browser.element('[data-qa="internet-sales-answer-answer"]').getText()
  }

  getChangeInRetailTurnoverSummary() {
    return browser.element('[data-qa="changes-in-retail-turnover-answer-answer"]').getText()
  }

  getChangeMaleEmployeesOver30Hours() {
    return browser.element('[data-qa="male-employees-over-30-hours-answer"]').getText()
  }

  editLinkChangeInRetailTurnover() {
    browser.click('[data-qa="changes-in-retail-turnover-answer-edit"]')
  }

  editLinkChangeInternetSales() {
    browser.click('[data-qa="internet-sales-answer-edit"]')
  }

  editLinkChangeMaleEmployeesOver30Hours() {
    browser.click('[data-qa="male-employees-over-30-hours-edit"]')
  }

}

export default new RSISummaryPage()
