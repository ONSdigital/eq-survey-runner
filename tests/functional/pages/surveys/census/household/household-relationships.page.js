import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class HouseholdRelationshipsPage extends MultipleChoiceWithOtherPage {

  clickHusbandOrWife() {
    browser.element('[id="household-relationships-answer-1"]').click()
    return this
  }

}

export default new HouseholdRelationshipsPage()
