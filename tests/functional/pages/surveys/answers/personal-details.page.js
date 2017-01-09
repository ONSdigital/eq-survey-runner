import QuestionPage from '../question.page'

class PersonalDetailsPage extends QuestionPage {

  constructor() {
    super('personal-details-block')
  }

  setFirstName(firstName) {
    browser.setValue('[name="first-name-answer"]', firstName)
    return this
  }

  setSurname(firstName) {
    browser.setValue('[name="surname-answer"]', firstName)
    return this
  }

}

export default new PersonalDetailsPage()
