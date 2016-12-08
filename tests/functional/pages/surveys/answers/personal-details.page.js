import QuestionPage from '../question.page'

class PersonalDetailsPage extends QuestionPage {

  constructor() {
    super('personal_details_block')
  }

  setFirstName(firstName) {
    browser.setValue('[name="first_name_answer"]', firstName)
    return this
  }

  setSurname(firstName) {
    browser.setValue('[name="surname_answer"]', firstName)
    return this
  }

}

export default new PersonalDetailsPage()
