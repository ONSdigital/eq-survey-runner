// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class TypeOfFlatPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('type-of-flat')
  }

  clickTypeOfFlatAnswerInAPurposeBuiltBlockOfFlatsOrTenement() {
    browser.element('[id="type-of-flat-answer-0"]').click()
    return this
  }

  clickTypeOfFlatAnswerPartOfAConvertedOrSharedHouseIncludingBedsits() {
    browser.element('[id="type-of-flat-answer-1"]').click()
    return this
  }

  clickTypeOfFlatAnswerInACommercialBuildingForExampleInAnOfficeBuildingHotelOrOverAShop() {
    browser.element('[id="type-of-flat-answer-2"]').click()
    return this
  }

}

export default new TypeOfFlatPage()
