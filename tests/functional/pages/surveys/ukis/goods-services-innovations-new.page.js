// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class GoodsServicesInnovationsNewPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('goods-services-innovations-new')
  }

  clickGoodsServicesInnovationsNewAnswerYes() {
    browser.element('[id="goods-services-innovations-new-answer-0"]').click()
    return this
  }

  clickGoodsServicesInnovationsNewAnswerNo() {
    browser.element('[id="goods-services-innovations-new-answer-1"]').click()
    return this
  }

}

export default new GoodsServicesInnovationsNewPage()
