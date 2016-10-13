import SummaryPage from '../../summary.page'

class MultipleAnswerSummaryPage {

  getFirstName() {
    return browser.element('[id="summary-0-0-0-answer"]').getText()
  }

  editSurname() {
    browser.element('[href="personal_details_block#surname_answer"]').click()
  }

  getSurname() {
    return browser.element('[id="summary-0-0-1-answer"]').getText()
  }

}

export default new MultipleAnswerSummaryPage()
