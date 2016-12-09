// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-12 22:01:11.832777 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class SelfContainedAccommodationPage extends MultipleChoiceWithOtherPage {

  clickSelfContainedAccommodationAnswerYesAllTheRoomsAreBehindADoorThatOnlyThisHouseholdCanUse() {
    browser.element('[id="self-contained-accommodation-answer-1"]').click()
    return this
  }

  clickSelfContainedAccommodationAnswerNo() {
    browser.element('[id="self-contained-accommodation-answer-2"]').click()
    return this
  }

}

export default new SelfContainedAccommodationPage()
