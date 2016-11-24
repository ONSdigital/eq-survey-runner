import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class SelfContainedAccommodationPage extends MultipleChoiceWithOtherPage {

  clickYesAllTheRoomsAreBehindADoorThatOnlyThisHouseholdCanUse() {
    browser.element('[id="self-contained-accommodation-answer-1"]').click()
    return this
  }

  clickNo() {
    browser.element('[id="self-contained-accommodation-answer-2"]').click()
    return this
  }

}

export default new SelfContainedAccommodationPage()
