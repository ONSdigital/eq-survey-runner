import SummaryPage from '../../summary.page'

class RadioSummaryPage extends SummaryPage {

  getBreakfastAnswer() {
    return browser.element('[data-qa="favourite-breakfast-answer"]').getText()
  }
  getLunchAnswer() {
    return browser.element('[data-qa="favourite-lunch-answer"]').getText()
  }

}

export default new RadioSummaryPage()
