import SummaryPage from '../../summary.page'

class CheckboxSummaryPage extends SummaryPage {

  getMandatoryAnswer() {
    return browser.element('[data-qa="mandatory-checkbox-answer-answer"]').getText();
  }

  getNonMandatoryAnswer() {
    return browser.element('[data-qa="non-mandatory-checkbox-answer-answer"]').getText();
  }

  getMandatoryOtherAnswer() {
    return browser.element('[data-qa="other-answer-mandatory-answer"]').getText();
  }

  getNonMandatoryOtherAnswer() {
    return browser.element('[data-qa="other-answer-non-mandatory-answer"]').getText();
  }

}

export default new CheckboxSummaryPage()
