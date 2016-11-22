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
    var household_names = [];
    var elements = browser.elements('[data-qa="household-full-name-answer"]');
    elements.value.forEach((elem) => {
        household_names.push(browser.elementIdText(elem.ELEMENT).value)
    });
    return household_names
  }
}

export default new HouseholdCompositionSummary()
