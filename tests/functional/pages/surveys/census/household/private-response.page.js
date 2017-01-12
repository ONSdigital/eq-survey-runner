// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class PrivateResponsePage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('private-response')
  }

  clickPrivateResponseAnswerNoIDoNotWantToRequestAPersonalForm() {
    browser.element('[id="private-response-answer-0"]').click()
    return this
  }

  clickPrivateResponseAnswerYesIWantToRequestAPersonalForm() {
    browser.element('[id="private-response-answer-1"]').click()
    return this
  }

}

export default new PrivateResponsePage()
