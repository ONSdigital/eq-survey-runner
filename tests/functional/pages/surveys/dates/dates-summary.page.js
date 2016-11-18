import SummaryPage from '../../summary.page'

class RSISummaryPage extends SummaryPage {

  getDateRangeSummary() {
    return browser.element('[data-qa="5b12aea2-ae3b-467d-9291-4d803a444d25-answer"]').getText()
  }

  getMonthYearDateSummary() {
    return browser.element('[data-qa="eade17ef-3ec6-46c2-afc7-dffeb07e2e5e-answer"]').getText()
  }

  getDateOfBirth() {
    return browser.element('[data-qa="a51b1c7b-3f25-49dd-9275-2ea742eee510-answer"]').getText()
  }

  getNonMandatoryDate() {
    return browser.element('[data-qa="98fa9cec-e0bb-471e-80e3-1ff3d9242ef8-answer"]').getText()
  }
}

export default new RSISummaryPage()
