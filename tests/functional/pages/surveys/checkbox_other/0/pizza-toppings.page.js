import QuestionPage from '../../question.page'

class PizzaToppingsPage extends QuestionPage {

  selectOther() {
      browser.click('input[id="ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c-6"]');
      return this;
  }

  inputOtherValue(text) {
      browser.setValue('input[id="ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c-6-other"]', text);
      return this;
  }

}

export default new PizzaToppingsPage()
