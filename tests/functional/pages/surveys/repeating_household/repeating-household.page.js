import QuestionPage from '../question.page'

class RepeatingHouseholdPage extends QuestionPage {

  getDisplayedName() {
    return browser.getText('h1[class="section__title saturn"]')
  }

}

export default new RepeatingHouseholdPage()
