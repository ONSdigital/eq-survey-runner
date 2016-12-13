// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-12 22:01:11.821764 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class ElsePermanentOrFamilyHomePage extends MultipleChoiceWithOtherPage {

  clickElsePermanentOrFamilyHomeAnswerSomeoneLivesHereAsTheirPermanentHome() {
    browser.element('[id="else-permanent-or-family-home-answer-1"]').click()
    return this
  }

  clickElsePermanentOrFamilyHomeAnswerNoOneLivesHereAsTheirPermanentHome() {
    browser.element('[id="else-permanent-or-family-home-answer-2"]').click()
    return this
  }

}

export default new ElsePermanentOrFamilyHomePage()
