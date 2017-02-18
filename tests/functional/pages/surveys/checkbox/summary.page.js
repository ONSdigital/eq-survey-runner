import SummaryPage from '../../summary.page'

class CheckboxSummaryPage extends SummaryPage {

  getPage1Answer() {
    return browser.element('[data-qa="ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c-answer"]').getText();
  }

  getPage2Answer() {
    return browser.element('[data-qa="ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23-answer"]').getText();
  }

  getPage1OtherAnswer() {
    return browser.element('[data-qa="other-answer-mandatory-answer"]').getText();
  }

  getPage2OtherAnswer() {
    return browser.element('[data-qa="other-answer-non-mandatory-answer"]').getText();
  }
}

export default new CheckboxSummaryPage()
