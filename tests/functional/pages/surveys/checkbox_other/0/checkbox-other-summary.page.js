import SummaryPage from '../../../summary.page'

class CheckboxOtherSummaryPage extends SummaryPage {

  getPizzaToppingAnswer() {
      var answer = browser.element('#summary-0-0-0-answer');
      return answer.getText();
  }

}

export default new CheckboxOtherSummaryPage()
