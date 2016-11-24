import QuestionPage from '../question.page'

class HouseholdRelationshipPage extends QuestionPage {

  getRelationshipLabelAt(index) {
    var id = this.buildAnswerId('#label-who-is-related', index)
    return browser.element(id).getText()
  }

  setHusbandOrWifeRelationship(index, relationshipIndex) {
    var id = this.buildRelationshipAnswerId(index, 1)
    browser.element(id).click()
    return this
  }

  setPartnerRelationship(index, relationshipIndex) {
    var id = this.buildRelationshipAnswerId(index, 2)
    browser.element(id).click()
    return this
  }

  setSonOrDaughterRelationship(index, relationshipIndex) {
    var id = this.buildRelationshipAnswerId(index, 4)
    browser.element(id).click()
    return this
  }

  buildRelationshipAnswerId(index, relationshipId) {
    var id = this.buildAnswerId('#who-is-related', index)
    id += '-' + relationshipId
    return id
  }

  buildAnswerId(answerId, index) {
    if (index > 0) {
      answerId += '_' + index
    }
    return answerId
  }

}

export default new HouseholdRelationshipPage()
