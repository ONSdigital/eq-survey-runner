import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class OwnOrRentPage extends MultipleChoiceWithOtherPage {

  clickOwnsOutright() {
    browser.element('[id="own-or-rent-answer-1"]').click()
    return this
  }

  clickOwnsWithAMortgageOrLoan() {
    browser.element('[id="own-or-rent-answer-2"]').click()
    return this
  }

  clickPartOwnsAndPartRentsSharedOwnership() {
    browser.element('[id="own-or-rent-answer-3"]').click()
    return this
  }

  clickRentsWithOrWithoutHousingBenefit() {
    browser.element('[id="own-or-rent-answer-4"]').click()
    return this
  }

  clickLivesHereRentFree() {
    browser.element('[id="own-or-rent-answer-5"]').click()
    return this
  }

}

export default new OwnOrRentPage()
