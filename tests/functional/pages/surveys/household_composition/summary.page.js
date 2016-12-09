import SummaryPage from '../../summary.page'

class HouseholdCompositionSummary extends SummaryPage {

  clickEdit() {
    browser.click('[data-qa="first-name-edit"]')
    return this
  }

  getFirstName(index) {
    return this.getFirstNames()[index]
  }

  getMiddleName(index) {
    return this.getMiddleNames()[index]
  }

  getLastName(index) {
    return this.getLastNames()[index]
  }

  getElementText(name, index) {
    return this.getElementTextForAnswer(name)[index]
  }

  getFirstNames() {
    return this.getElementTextForAnswer('first-name')
  }

  getMiddleNames() {
    return this.getElementTextForAnswer('middle-names')
  }

  getLastNames() {
    return this.getElementTextForAnswer('last-name')
  }

  getElementTextForAnswer(answer) {
    var householdNames = []
    var elements = browser.elements('[data-qa="' + answer + '-answer"]')
    elements.value.forEach((elem) => {
      householdNames.push(browser.elementIdText(elem.ELEMENT).value)
    })
    return householdNames
  }
}

export default new HouseholdCompositionSummary()
