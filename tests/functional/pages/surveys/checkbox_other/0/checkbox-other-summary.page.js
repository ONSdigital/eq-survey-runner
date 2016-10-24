import QuestionPage from '../../question.page'

class CheckboxOtherSummaryPage extends QuestionPage {

  getPizzaToppingAnswer() {
      var answer = browser.element('#summary-0-0-0-answer');
      return answer.getText();
  }

}

export default new CheckboxOtherSummaryPage()
