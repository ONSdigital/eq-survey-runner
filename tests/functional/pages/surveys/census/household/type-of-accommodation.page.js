import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class TypeOfAccommodationPage extends MultipleChoiceWithOtherPage {

  clickTypeOfAccommodationAnswerWholeHouseOrBungalow() {
    browser.element('[id="type-of-accommodation-answer-1"]').click()
    return this
  }

  clickTypeOfAccommodationAnswerFlatMaisonetteOrApartment() {
    browser.element('[id="type-of-accommodation-answer-2"]').click()
    return this
  }

  clickTypeOfAccommodationAnswerCaravanOrOtherMobileOrTemporaryStructure() {
    browser.element('[id="type-of-accommodation-answer-3"]').click()
    return this
  }

}

export default new TypeOfAccommodationPage()
