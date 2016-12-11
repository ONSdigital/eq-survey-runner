import SummaryPage from '../../summary.page'

class HouseholdCompositionSummary extends SummaryPage {

  clickAddAnother() {
    browser.click('[name="household-composition-add-another"][value="No"]')
    return this
  }

  submit() {
    browser.click('.qa-btn-submit')
    return this
  }

  isNameDisplayed(name) {
    return browser.element('#further-section ul li').getText() === name
  }

  getElementTextForAnswer(answer) {
    var householdNames = []
    var elements = browser.elements('#further-section ul li')

    elements.value.forEach((elem) => {
      householdNames.push(browser.elementIdText(elem.ELEMENT).value)
    })
    return householdNames
  }
}

export default new HouseholdCompositionSummary()
