// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class IntroducingSignificantlyImprovedGoodsPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('introducing-significantly-improved-goods')
  }

  clickIntroducingSignificantlyImprovedGoodsAnswerYes() {
    browser.element('[id="introducing-significantly-improved-goods-answer-0"]').click()
    return this
  }

  clickIntroducingSignificantlyImprovedGoodsAnswerNo() {
    browser.element('[id="introducing-significantly-improved-goods-answer-1"]').click()
    return this
  }

}

export default new IntroducingSignificantlyImprovedGoodsPage()
