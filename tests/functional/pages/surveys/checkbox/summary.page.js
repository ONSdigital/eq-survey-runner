import SummaryPage from '../../summary.page'

class CheckboxSummaryPage extends SummaryPage {

  getPage1Answer() {
      var answer = browser.element('#summary-0-0-0-answer');
      return answer.getText();
  }

  getPage2Answer() {
    var answer = browser.element('#summary-1-0-0-answer');
    return answer.getText();
  }

}

export default new CheckboxSummaryPage()
