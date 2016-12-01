import SummaryPage from '../../summary.page'

class HouseholdCompositionSummary extends SummaryPage {

  clickAddAnother() {
    browser.click('[name="household-composition-add-another"]')
    return this
  }

  submit() {
    browser.click('.qa-btn-submit')
    return this
  }

  isNameDisplayed(name) {
    return browser.element('.box--entity__person').getText() === name
  }

  getHouseholdNames() {
    var householdNames = []
    var elements = browser.elements('.box--entity__person')
    elements.value.forEach((elem) => {
      householdNames.push(browser.elementIdText(elem.ELEMENT).value)
    })
    return householdNames
  }
}

export default new HouseholdCompositionSummary()
