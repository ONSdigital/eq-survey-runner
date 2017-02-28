import QuestionPage from '../question.page'

class FinalConfirmationSurveyPage extends QuestionPage {

  isOpen() {
    return browser.isExisting('.qa-questionnaire-form')
  }

  setBreakfastFood(food) {
    browser.setValue('[name="breakfast-answer"]', food)
    return this
  }

}

export default new FinalConfirmationSurveyPage()
