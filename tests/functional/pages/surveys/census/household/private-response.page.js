// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-12 22:01:11.845991 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class PrivateResponsePage extends MultipleChoiceWithOtherPage {

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
