import SummaryPage from '../../summary.page'

class RadioSummaryPage extends SummaryPage {

  getPage1Answer() {
    return browser.element('[data-qa="other-answer-mandatory-answer"]').getText()
  }

}

export default new RadioSummaryPage()
