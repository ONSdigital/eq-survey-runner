// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class DoYouWantToSkipPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('do-you-want-to-skip')
  }

  clickDoYouWantToSkipAnswerYes() {
    browser.element('[id="do-you-want-to-skip-answer-0"]').click()
    return this
  }

  clickDoYouWantToSkipAnswerNo() {
    browser.element('[id="do-you-want-to-skip-answer-1"]').click()
    return this
  }

}

export default new DoYouWantToSkipPage()
