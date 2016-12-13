// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-12 22:01:11.828958 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class TypeOfAccommodationPage extends MultipleChoiceWithOtherPage {

  clickTypeOfAccommodationAnswerWholeHouseOrBungalow() {
    browser.element('[id="type-of-accommodation-answer-1"]').click()
    return this
  }

  clickTypeOfAccommodationAnswerFlatMaisonetteOrApartmentIncludingBedsits() {
    browser.element('[id="type-of-accommodation-answer-2"]').click()
    return this
  }

  clickTypeOfAccommodationAnswerCaravanOrOtherMobileOrTemporaryStructure() {
    browser.element('[id="type-of-accommodation-answer-3"]').click()
    return this
  }

}

export default new TypeOfAccommodationPage()
