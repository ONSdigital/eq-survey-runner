import QuestionPage from '../question.page'

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
    var field = "414699da-1667-44fd-8e98-7606966884db"
    if (index > 0) {
        field = field + "_" + index
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
