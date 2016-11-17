import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class TypeOfHousePage extends MultipleChoiceWithOtherPage {

  clickTypeOfHouseAnswerDetached() {
    browser.element('[id="type-of-house-answer-1"]').click()
    return this
  }

  clickTypeOfHouseAnswerSemiDetached() {
    browser.element('[id="type-of-house-answer-2"]').click()
    return this
  }

  clickTypeOfHouseAnswerTerraced() {
    browser.element('[id="type-of-house-answer-3"]').click()
    return this
  }

}

export default new TypeOfHousePage()
