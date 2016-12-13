// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-12 22:01:11.826456 - DO NOT EDIT!!! <<<

// HAND EDITED VERSION - NEEDS TO BE ADDED TO GENERATOR

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class HouseholdRelationshipsPage extends MultipleChoiceWithOtherPage {

  clickHouseholdRelationshipsAnswerHusbandOrWife() {
    browser.element('[id="household-relationships-answer-1"]').click()
    return this
  }

}

export default new HouseholdRelationshipsPage()
