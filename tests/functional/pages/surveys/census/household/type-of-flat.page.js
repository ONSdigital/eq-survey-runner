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

}

export default new TypeOfFlatPage()
