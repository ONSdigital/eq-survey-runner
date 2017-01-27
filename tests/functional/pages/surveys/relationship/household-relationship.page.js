import QuestionPage from '../question.page'

class HouseholdRelationshipPage extends QuestionPage {

  getRelationshipLabelAt(index) {
    const elementId = browser.elements('[data-qa="relationship-title"]').value[index]
    return browser.elementIdText(elementId.ELEMENT).value
  }

  setHusbandOrWifeRelationship(index, relationshipIndex) {
    const id = this.buildRelationshipAnswerId(index, 0)
    browser.waitForExist(id)
    browser.element(id).click().pause(300)
    return this
  }

  setSonOrDaughterRelationship(index, relationshipIndex) {
    const id = this.buildRelationshipAnswerId(index, 3)
    browser.waitForExist(id)
    browser.element(id).click().pause(300)
    return this
  }

  buildRelationshipAnswerId(index, relationshipId) {
    const id = '#who-is-related-' + index + '-' + relationshipId
    return id
  }

  toggleEditCloseButton(index) {
    let btnId = browser.elements('[data-qa="relationship-close-btn"]').value[index]
    browser.elementIdClick(btnId.ELEMENT)
    return this
  }

  submit() {
    browser.submitForm('.qa-questionnaire-form')
    return this
  }

}

export default new HouseholdRelationshipPage()
