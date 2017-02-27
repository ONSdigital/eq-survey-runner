import SummaryPage from '../../summary.page'

class TimeoutSummaryPage {

  isOpen() {
    return SummaryPage.isOpen()
  }

  getTimeoutAnswer() {
    return browser.element('[data-qa="timeout-answer-answer"]').getText()
  }

}

export default new TimeoutSummaryPage()
