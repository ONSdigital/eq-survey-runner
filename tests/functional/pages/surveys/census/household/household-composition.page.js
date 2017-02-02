// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../../question.page'

class HouseholdCompositionPage extends QuestionPage {

  constructor() {
    super('household-composition')
  }

  addPerson() {
    browser.click('button[name="action[add_answer]"]')
    return this
  }

  removePerson(index) {
    browser.click('button[value="' + index + '"]')
    browser.waitUntil(() => {
      return !browser.isVisible('button[value="' + index + '"]')
    }, 5000, 'Person not removed')
    return this
  }

  setFirstName(value, index = 0) {
    var field = 'household-' + index + '-first-name'
    browser.setValue('[name="' + field + '"]', value)
    return this
  }

  getFirstName(index) {
    var field = 'household-' + index + '-first-name'
    browser.element('[name="' + field + '"]').getValue()
    return this
  }

  setMiddleNames(value, index = 0) {
    var field = 'household-' + index + '-middle-names'
    browser.setValue('[name="' + field + '"]', value)
    return this
  }

  getMiddleNames(index) {
    var field = 'household-' + index + '-middle-names'
    browser.element('[name="' + field + '"]').getValue()
    return this
  }

  setLastName(value, index = 0) {
    var field = 'household-' + index + '-last-name'
    browser.setValue('[name="' + field + '"]', value)
    return this
  }

  getLastName(index) {
    var field = 'household-' + index + '-last-name'
    browser.element('[name="' + field + '"]').getValue()
    return this
  }

}

export default new HouseholdCompositionPage()
