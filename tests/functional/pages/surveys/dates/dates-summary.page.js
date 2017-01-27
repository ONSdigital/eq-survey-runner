import SummaryPage from '../../summary.page'

class RSISummaryPage extends SummaryPage {

  getDateRangeSummary() {
    return browser.element('[data-qa="date-range-from-answer"]').getText()
  }

  getMonthYearDateSummary() {
    return browser.element('[data-qa="month-year-answer-answer"]').getText()
  }

  getDateOfBirth() {
    return browser.element('[data-qa="single-date-answer-answer"]').getText()
  }

  getNonMandatoryDate() {
    return browser.element('[data-qa="non-mandatory-date-answer-answer"]').getText()
  }
}

export default new RSISummaryPage()
