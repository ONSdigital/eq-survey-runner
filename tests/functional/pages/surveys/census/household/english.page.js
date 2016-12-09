// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-12 22:01:11.899382 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class EnglishPage extends MultipleChoiceWithOtherPage {

  clickEnglishAnswerVeryWell() {
    browser.element('[id="english-answer-1"]').click()
    return this
  }

  clickEnglishAnswerWell() {
    browser.element('[id="english-answer-2"]').click()
    return this
  }

  clickEnglishAnswerNotWell() {
    browser.element('[id="english-answer-3"]').click()
    return this
  }

  clickEnglishAnswerNotAtAll() {
    browser.element('[id="english-answer-4"]').click()
    return this
  }

}

export default new EnglishPage()
