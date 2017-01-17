import QuestionPage from '../question.page'

class HouseholdCompositionPage extends QuestionPage {

  setPersonName(index, first = '', middle = '', last = '') {
    return this.setFirstName(index, first).setMiddleNames(index, middle).setLastName(index, last)
  }

  setFirstName(index, value) {
    browser.setValue(this.getInputSelector(index, 'first_name'), value)
    return this
  }

  setMiddleNames(index, value) {
    browser.setValue(this.getInputSelector(index, 'middle_names'), value)
    return this
  }

  setLastName(index, value) {
    browser.setValue(this.getInputSelector(index, 'last_name'), value)
    return this
  }

  getInputSelector(index, name) {
    return 'input[name="' + this.getInputFieldName(index, name) + '"]'
  }

  isInputVisible(index, name) {
    return browser.isVisible(this.getInputSelector(index, name))
  }

  getInputFieldName(index, name) {
    var field = 'household-' + index + '-' + name
    return field
  }

  addPerson() {
    browser.click('button[name="action[add_answer]"]')
    return this
  }

  removePerson(index) {
    browser.click('button[value="' + index + '"]')
    return this
  }

}

export default new HouseholdCompositionPage()
