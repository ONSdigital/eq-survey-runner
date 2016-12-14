// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.753412 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class PrivateResponsePage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('private-response')
  }

  clickPrivateResponseAnswerNoIDoNotWantToRequestAPersonalForm() {
    browser.element('[id="private-response-answer-1"]').click()
    return this
  }

  clickPrivateResponseAnswerYesIWantToRequestAPersonalForm() {
    browser.element('[id="private-response-answer-2"]').click()
    return this
  }

}

export default new PrivateResponsePage()
