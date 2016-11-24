import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class TypeOfAccommodationPage extends MultipleChoiceWithOtherPage {

  clickWholeHouseOrBungalow() {
    browser.element('[id="type-of-accommodation-answer-1"]').click()
    return this
  }

  clickFlatMaisonetteOrApartment() {
    browser.element('[id="type-of-accommodation-answer-2"]').click()
    return this
  }

  clickCaravanOrOtherMobileOrTemporaryStructure() {
    browser.element('[id="type-of-accommodation-answer-3"]').click()
    return this
  }

}

export default new TypeOfAccommodationPage()
