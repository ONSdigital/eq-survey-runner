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

  setSelfContainedAccommodationAnswer(value) {
    browser.setValue('[name="self-contained-accommodation-answer"]', value)
    return this
  }

  getSelfContainedAccommodationAnswer(value) {
    return browser.element('[name="self-contained-accommodation-answer"]').getValue()
  }

}

export default new SelfContainedAccommodationPage()
