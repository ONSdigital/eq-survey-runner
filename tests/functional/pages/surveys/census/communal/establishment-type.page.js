import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class EstablishmentTypePage extends MultipleChoiceWithOtherPage {

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
