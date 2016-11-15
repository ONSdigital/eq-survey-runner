import SummaryPage from '../../summary.page'

class HouseholdCompositionSummary extends SummaryPage {

  isNameDisplayed() {
    return browser.element('[data-qa="ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c-answer"]').getText()
  }

}

export default new HouseholdCompositionSummary()
