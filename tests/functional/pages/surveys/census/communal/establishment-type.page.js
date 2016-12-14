// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-14 14:19:14.064568 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class EstablishmentTypePage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('establishment-type')
  }

  clickEstablishmentTypeAnswerHotel() {
    browser.element('[id="establishment-type-answer-1"]').click()
    return this
  }

  clickEstablishmentTypeAnswerGuestHouse() {
    browser.element('[id="establishment-type-answer-2"]').click()
    return this
  }

  clickEstablishmentTypeAnswerBB() {
    browser.element('[id="establishment-type-answer-3"]').click()
    return this
  }

  clickEstablishmentTypeAnswerInnPub() {
    browser.element('[id="establishment-type-answer-4"]').click()
    return this
  }

  clickEstablishmentTypeAnswerOther() {
    browser.element('[id="establishment-type-answer-5"]').click()
    return this
  }

}

export default new EstablishmentTypePage()
