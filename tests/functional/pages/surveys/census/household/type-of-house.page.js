// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class TypeOfHousePage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('type-of-house')
  }

  clickTypeOfHouseAnswerDetached() {
    browser.element('[id="type-of-house-answer-0"]').click()
    return this
  }

  clickTypeOfHouseAnswerSemiDetached() {
    browser.element('[id="type-of-house-answer-1"]').click()
    return this
  }

  clickTypeOfHouseAnswerTerraced() {
    browser.element('[id="type-of-house-answer-2"]').click()
    return this
  }

}

export default new TypeOfHousePage()
