import QuestionPage from '../question.page'

class RepeatingHouseholdPage extends QuestionPage {

  getDisplayedName() {
    return browser.getText('[data-qa="section-title"]')
  }

}

export default new RepeatingHouseholdPage()
