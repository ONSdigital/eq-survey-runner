import QuestionPage from '../question.page'

class OtherOptionsRadioPage extends QuestionPage {

  clickYes() {
    browser.element('[name="7587qe9b-f24e-4dc0-ac94-66118b896c10"]').click()
    return this
  }

}

export default new OtherOptionsRadioPage()
