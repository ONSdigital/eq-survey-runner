import SummaryPage from '../../summary.page'

class MultipleAnswerSummaryPage {

  getFirstName() {
    return browser.element('[data-qa="first_name_answer-answer"]').getText()
  }

  editSurname() {
    browser.element('[data-qa="surname_answer-edit"]').click()
  }

  getSurname() {
    return browser.element('[data-qa="surname_answer-answer"]').getText()
  }

}

export default new MultipleAnswerSummaryPage()
