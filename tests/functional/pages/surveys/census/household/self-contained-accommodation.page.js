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
