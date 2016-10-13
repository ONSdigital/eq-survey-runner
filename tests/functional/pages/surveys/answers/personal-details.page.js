import QuestionPage from '../question.page'

class PersonalDetailsPage extends QuestionPage {

  isOpen() {
    const url = browser.url().value
    return url.indexOf('personal_details_block') > -1
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
