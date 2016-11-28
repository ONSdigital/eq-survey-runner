import QuestionPage from '../../question.page'

class EmployersBusinessPage extends QuestionPage {

  setEmployersBusinessAnswer(value) {
    browser.setValue('[name="employers-business-answer"]', value)
    return this
  }

  getEmployersBusinessAnswer(value) {
    return browser.element('[name="employers-business-answer"]').getValue()
  }

}

export default new EmployersBusinessPage()
