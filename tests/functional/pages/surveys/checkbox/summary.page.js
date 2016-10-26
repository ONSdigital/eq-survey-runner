import SummaryPage from '../../summary.page'

class CheckboxSummaryPage extends SummaryPage {

  getPage1Answer() {
      var answer = browser.element('[data-qa="ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c-answer"');
      return answer.getText();
  }

  getPage2Answer() {
    var answer = browser.element('[data-qa="ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23-answer"');
    return answer.getText();
  }

}

export default new CheckboxSummaryPage()
