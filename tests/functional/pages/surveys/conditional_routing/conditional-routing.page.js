import QuestionPage from '../question.page'

class ConditionalRoutingPage extends QuestionPage {

  clickYes() {
    browser.element('input[value="yes"]').click()
    return this
  }

  clickNo() {
    browser.element('input[value="no"]').click()
    return this
  }

}

export default new ConditionalRoutingPage()
