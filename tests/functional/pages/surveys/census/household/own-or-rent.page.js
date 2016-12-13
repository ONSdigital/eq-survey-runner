// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-12 22:01:11.836810 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class OwnOrRentPage extends MultipleChoiceWithOtherPage {

  clickOwnOrRentAnswerOwnsOutright() {
    browser.element('[id="own-or-rent-answer-1"]').click()
    return this
  }

  clickOwnOrRentAnswerOwnsWithAMortgageOrLoan() {
    browser.element('[id="own-or-rent-answer-2"]').click()
    return this
  }

  clickOwnOrRentAnswerPartOwnsAndPartRentsSharedOwnership() {
    browser.element('[id="own-or-rent-answer-3"]').click()
    return this
  }

  clickOwnOrRentAnswerRentsWithOrWithoutHousingBenefit() {
    browser.element('[id="own-or-rent-answer-4"]').click()
    return this
  }

  clickOwnOrRentAnswerLivesHereRentFree() {
    browser.element('[id="own-or-rent-answer-5"]').click()
    return this
  }

}

export default new OwnOrRentPage()
