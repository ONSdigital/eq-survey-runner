import SummaryPage from '../../summary.page'

class OtherOptionsSummary extends SummaryPage {

  getOtherRadioSummary() {
    return browser.element('[data-qa="answer-0-0 answer-type-radio"]').getText()
  }

}

export default new OtherOptionsSummary()
