import QuestionPage from '../question.page'

class InterstitialSurveyPage extends QuestionPage {

  isOpen() {
    return browser.isExisting('.qa-questionnaire-form')
  }

  setBreakfastFood(food) {
    browser.setValue('[name="favourite-breakfast"]', food)
    return this
  }

  setLunchFood(lunch) {
    browser.setValue('[name="favourite-lunch"]', lunch)
    return this
  }

}

export default new InterstitialSurveyPage()
