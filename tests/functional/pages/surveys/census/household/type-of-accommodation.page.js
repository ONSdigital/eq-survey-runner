// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class TypeOfAccommodationPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('type-of-accommodation')
  }

  clickTypeOfAccommodationAnswerWholeHouseOrBungalow() {
    browser.element('[id="type-of-accommodation-answer-0"]').click()
    return this
  }

  clickTypeOfAccommodationAnswerFlatMaisonetteOrApartmentIncludingBedsits() {
    browser.element('[id="type-of-accommodation-answer-1"]').click()
    return this
  }

  clickTypeOfAccommodationAnswerCaravanOrOtherMobileOrTemporaryStructure() {
    browser.element('[id="type-of-accommodation-answer-2"]').click()
    return this
  }

}

export default new TypeOfAccommodationPage()
