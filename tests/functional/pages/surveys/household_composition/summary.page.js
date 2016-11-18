import SummaryPage from '../../summary.page'

class HouseholdCompositionSummary extends SummaryPage {

  clickEdit() {
    browser.click('[data-qa="household-full-name-edit"]')
    return this
  }

  isNameDisplayed(name) {
    return browser.element('[data-qa="household-full-name-answer"]').getText() === name
  }

  areNamesDisplayed(names) {
    var allNamesDisplayed = true
    var elements = browser.elements('[data-qa="household-full-name-answer"]')
    var name
    for (name in names) {
      var nameFound = false
      var i
      for (i = 0; i < elements.length; i++) {
        if (elements[i].getText() === name) {
          nameFound = true
        }
        allNamesDisplayed &= nameFound
        if (!allNamesDisplayed) {
          break
        }
      }
    }
    return allNamesDisplayed
  }

}

export default new HouseholdCompositionSummary()
