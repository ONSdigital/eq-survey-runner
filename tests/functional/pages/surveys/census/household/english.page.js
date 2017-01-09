// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class EnglishPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('english')
  }

  clickEnglishAnswerVeryWell() {
    browser.element('[id="english-answer-0"]').click()
    return this
  }

  clickEnglishAnswerWell() {
    browser.element('[id="english-answer-1"]').click()
    return this
  }

  clickEnglishAnswerNotWell() {
    browser.element('[id="english-answer-2"]').click()
    return this
  }

  clickEnglishAnswerNotAtAll() {
    browser.element('[id="english-answer-3"]').click()
    return this
  }

}

export default new EnglishPage()
