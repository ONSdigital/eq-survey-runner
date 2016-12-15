// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.724527 - DO NOT EDIT!!! <<<

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
    return this
  }

  setFirstName(value, index = 0) {
    var field = 'first-name'
    if (index > 0) {
      field = field + '_' + index
    }
    browser.setValue('[name="' + field + '"]', value)
    return this
  }

  getFirstName(index) {
    var field = 'first-name'
    if (index > 0) {
      field = field + '_' + index
    }
    browser.element('[name="' + field + '"]').getValue()
    return this
  }

  setMiddleNames(value, index = 0) {
    var field = 'middle-names'
    if (index > 0) {
      field = field + '_' + index
    }
    browser.setValue('[name="' + field + '"]', value)
    return this
  }

  getMiddleNames(index) {
    var field = 'middle-names'
    if (index > 0) {
      field = field + '_' + index
    }
    browser.element('[name="' + field + '"]').getValue()
    return this
  }

  setLastName(value, index = 0) {
    var field = 'last-name'
    if (index > 0) {
      field = field + '_' + index
    }
    browser.setValue('[name="' + field + '"]', value)
    return this
  }

  getLastName(index) {
    var field = 'last-name'
    if (index > 0) {
      field = field + '_' + index
    }
    browser.element('[name="' + field + '"]').getValue()
    return this
  }

}

export default new HouseholdCompositionPage()
