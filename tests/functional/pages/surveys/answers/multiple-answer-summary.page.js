import SummaryPage from '../../summary.page'

class MultipleAnswerSummaryPage {

  getFirstName() {
    return browser.element('[data-qa="first-name-answer-answer"]').getText()
  }

  editSurname() {
    browser.element('[data-qa="surname-answer-edit"]').click()
  }

  getSurname() {
    return browser.element('[data-qa="surname-answer-answer"]').getText()
  }

}

export default new MultipleAnswerSummaryPage()
