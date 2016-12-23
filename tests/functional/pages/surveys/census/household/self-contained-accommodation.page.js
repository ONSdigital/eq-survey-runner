// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class SelfContainedAccommodationPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('self-contained-accommodation')
  }

  clickSelfContainedAccommodationAnswerYesAllTheRoomsAreBehindADoorThatOnlyThisHouseholdCanUse() {
    browser.element('[id="self-contained-accommodation-answer-0"]').click()
    return this
  }

  clickSelfContainedAccommodationAnswerNo() {
    browser.element('[id="self-contained-accommodation-answer-1"]').click()
    return this
  }

}

export default new SelfContainedAccommodationPage()
