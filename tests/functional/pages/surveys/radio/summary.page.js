import SummaryPage from '../../summary.page'

class RadioSummaryPage extends SummaryPage {

  getMandatoryOtherAnswer() {
    return browser.element('[data-qa="other-answer-mandatory-answer"]').getText()
  }

  getMandatoryAnswer() {
    return browser.element('[data-qa="radio-mandatory-answer-answer"]').getText()
  }

}

export default new RadioSummaryPage()
