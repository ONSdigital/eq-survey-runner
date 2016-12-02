import QuestionPage from '../question.page'

class HouseholdRelationshipPage extends QuestionPage {

  getRelationshipLabelAt(index) {
    var elementId = browser.elements('[id="relationship-title"]').value[index]
    return browser.elementIdText(elementId.ELEMENT).value
  }

  setHusbandOrWifeRelationship(index, relationshipIndex) {
    var id = this.buildRelationshipAnswerId(index, 1)
    browser.element(id).click()
    return this
  }

  setSonOrDaughterRelationship(index, relationshipIndex) {
    var id = this.buildRelationshipAnswerId(index, 4)
    browser.element(id).click()
    return this
  }

  buildRelationshipAnswerId(index, relationshipId) {
    var id = '#who-is-related'
    if (index > 0) {
      id += '_' + index
    }
    id += '-' + relationshipId
    return id
  }

  submit() {
    browser.submitForm('.qa-questionnaire-form')
    return this
  }

}

export default new HouseholdRelationshipPage()
