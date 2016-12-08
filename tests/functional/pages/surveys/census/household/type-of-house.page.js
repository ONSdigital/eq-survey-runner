// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.732315 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class TypeOfHousePage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('type-of-house')
  }

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
