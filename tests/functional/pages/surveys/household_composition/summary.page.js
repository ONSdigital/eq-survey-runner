import SummaryPage from '../../summary.page'

class HouseholdCompositionSummary extends SummaryPage {

  clickEdit() {
    browser.click('[data-qa="household-full-name-edit"]')
    return this
  }

  isNameDisplayed(name) {
    return browser.element('[data-qa="household-full-name-answer"]').getText() === name
  }

  getHouseholdNames() {
    var householdNames = []
    var elements = browser.elements('[data-qa="household-full-name-answer"]')
    elements.value.forEach((elem) => {
      householdNames.push(browser.elementIdText(elem.ELEMENT).value)
    })
    return householdNames
  }
}

export default new HouseholdCompositionSummary()
