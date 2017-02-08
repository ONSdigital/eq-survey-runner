// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class NewGoodsServicesInnovationsPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('new-goods-services-innovations')
  }

  clickNewGoodsServicesInnovationsAnswerYes() {
    browser.element('[id="new-goods-services-innovations-answer-0"]').click()
    return this
  }

  clickNewGoodsServicesInnovationsAnswerNo() {
    browser.element('[id="new-goods-services-innovations-answer-1"]').click()
    return this
  }

}

export default new NewGoodsServicesInnovationsPage()
