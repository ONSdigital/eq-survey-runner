import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class TypeOfFlatPage extends MultipleChoiceWithOtherPage {

  clickInAPurposeBuiltBlockOfFlatsOrTenement() {
    browser.element('[id="type-of-flat-answer-1"]').click()
    return this
  }

  clickPartOfAConvertedOrSharedHouseIncludingBedsits() {
    browser.element('[id="type-of-flat-answer-2"]').click()
    return this
  }

  clickInACommercialBuildingForExampleInAnOfficeBuildingHotelOrOverAShop() {
    browser.element('[id="type-of-flat-answer-3"]').click()
    return this
  }

  setTypeOfFlatAnswer(value) {
    browser.setValue('[name="type-of-flat-answer"]', value)
    return this
  }

  getTypeOfFlatAnswer(value) {
    return browser.element('[name="type-of-flat-answer"]').getValue()
  }

}

export default new TypeOfFlatPage()
