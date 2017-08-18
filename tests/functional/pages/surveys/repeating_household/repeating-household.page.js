import QuestionPage from '../question.page'

class RepeatingHouseholdPage extends QuestionPage {

  getDisplayedName() {
    return browser.getText('[data-qa="block-title"]')
  }

}

export default new RepeatingHouseholdPage()
