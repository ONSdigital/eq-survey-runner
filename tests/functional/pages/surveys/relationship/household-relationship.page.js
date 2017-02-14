import QuestionPage from '../question.page'

class HouseholdRelationshipPage extends QuestionPage {

  setHusbandOrWifeRelationship(index, relationshipIndex) {
    browser.selectByValue('#who-is-related-0', 'Husband or wife')
    return this
  }

  setSonOrDaughterRelationship(index, relationshipIndex) {
    browser.selectByValue('#who-is-related-1', 'Son or daughter')
    return this
  }

  submit() {
    browser.submitForm('.qa-questionnaire-form')
    return this
  }

}

export default new HouseholdRelationshipPage()
