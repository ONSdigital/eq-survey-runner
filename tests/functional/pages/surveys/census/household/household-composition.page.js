import QuestionPage from '../../question.page'

class HouseholdCompositionPage extends QuestionPage {

  setPersonName(index, value) {
    browser.setValue(this.getInputSelector(index), value)
    return this
  }

  getInputSelector(index) {
    return 'input[name="' + this.getInputFieldName(index) + '"]'
  }

  isInputVisible(index) {
    return browser.isVisible(this.getInputSelector(index))
  }

  getInputFieldName(index) {
    var field = 'household-composition-answer'
    if (index > 0) {
      field = field + '_' + index
    }
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
