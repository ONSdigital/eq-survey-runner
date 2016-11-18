import QuestionPage from '../question.page'

class HouseholdCompositionPage extends QuestionPage {

  getRelationshipLabelAt(index) {
    var id = this.buildAnswerId('#legend-relationship', index)
    return browser.element(id).getText()
  }

  getQuestionTitle() {
    return browser.element('#title-relationship-question').getText()
  }

  setFatherRelationship(index, relationshipIndex) {
     var id = this.buildRelationshipAnswerId(index, 2)
     browser.element(id).click()
     return this
  }

  setSonRelationship(index, relationshipIndex) {
     var id = this.buildRelationshipAnswerId(index, 4)
     browser.element(id).click()
     return this
  }

  buildRelationshipAnswerId(index, relationshipId) {
     var id = this.buildAnswerId('#relationship', index)
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

export default new HouseholdCompositionPage()
