import QuestionPage from '../question.page'

class FinalConfirmationSurveyPage extends QuestionPage {

  isOpen() {
    return browser.isExisting('.qa-questionnaire-form')
  }

  setBreakfastFood(food) {
    browser.setValue('[name="ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c"]', food)
    return this
  }

}

export default new FinalConfirmationSurveyPage()
