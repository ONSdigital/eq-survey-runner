// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class EntityDevelopedTheseGoodsPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('entity-developed-these-goods')
  }

  clickGentityDevelopedTheseGoodsAnswerThisBusinessOrEnterpriseGroup() {
    browser.element('[id="gentity-developed-these-goods-answer-0"]').click()
    return this
  }

  clickGentityDevelopedTheseGoodsAnswerThisBusinessWithOtherBusinessesOrOrganisations() {
    browser.element('[id="gentity-developed-these-goods-answer-1"]').click()
    return this
  }

  clickGentityDevelopedTheseGoodsAnswerOtherBusinessesOrOrganisations() {
    browser.element('[id="gentity-developed-these-goods-answer-2"]').click()
    return this
  }

}

export default new EntityDevelopedTheseGoodsPage()
