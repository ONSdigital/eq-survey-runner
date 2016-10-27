import SummaryPage from '../../summary.page'

class RadioSummaryPage extends SummaryPage {

  getPage1Answer() {
    return browser.element('[data-qa="answer-0-0 answer-type-radio"]').getText()
  }

}

export default new RadioSummaryPage()
