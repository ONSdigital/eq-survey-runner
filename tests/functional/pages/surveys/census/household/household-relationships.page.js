import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class HouseholdRelationshipsPage extends MultipleChoiceWithOtherPage {

  clickHusbandOrWife() {
    browser.element('[id="household-relationships-answer-1"]').click()
    return this
  }

  setHouseholdRelationshipsAnswer(value) {
    browser.setValue('[name="household-relationships-answer"]', value)
    return this
  }

  getHouseholdRelationshipsAnswer(value) {
    return browser.element('[name="household-relationships-answer"]').getValue()
  }

}

export default new HouseholdRelationshipsPage()
