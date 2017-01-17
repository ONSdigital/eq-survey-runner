// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class ReligionPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('religion')
  }

  clickReligionAnswerNoReligion() {
    browser.element('[id="religion-answer-0"]').click()
    return this
  }

  clickReligionAnswerChristianIncludingChurchOfEnglandCatholicProtestantAndAllOtherChristianDenominations() {
    browser.element('[id="religion-answer-1"]').click()
    return this
  }

  clickReligionAnswerBuddhist() {
    browser.element('[id="religion-answer-2"]').click()
    return this
  }

  clickReligionAnswerHindu() {
    browser.element('[id="religion-answer-3"]').click()
    return this
  }

  clickReligionAnswerJewish() {
    browser.element('[id="religion-answer-4"]').click()
    return this
  }

  clickReligionAnswerMuslim() {
    browser.element('[id="religion-answer-5"]').click()
    return this
  }

  clickReligionAnswerSikh() {
    browser.element('[id="religion-answer-6"]').click()
    return this
  }

  clickReligionAnswerOther() {
    browser.element('[id="religion-answer-7"]').click()
    return this
  }

  setReligionAnswerOtherText(value) {
    browser.setValue('[id="religion-answer-other"]', value)
    return this
  }

  clickReligionWelshAnswerNoReligion() {
    browser.element('[id="religion-welsh-answer-0"]').click()
    return this
  }

  clickReligionWelshAnswerChristianAllDenominations() {
    browser.element('[id="religion-welsh-answer-1"]').click()
    return this
  }

  clickReligionWelshAnswerBuddhist() {
    browser.element('[id="religion-welsh-answer-2"]').click()
    return this
  }

  clickReligionWelshAnswerHindu() {
    browser.element('[id="religion-welsh-answer-3"]').click()
    return this
  }

  clickReligionWelshAnswerJewish() {
    browser.element('[id="religion-welsh-answer-4"]').click()
    return this
  }

  clickReligionWelshAnswerMuslim() {
    browser.element('[id="religion-welsh-answer-5"]').click()
    return this
  }

  clickReligionWelshAnswerSikh() {
    browser.element('[id="religion-welsh-answer-6"]').click()
    return this
  }

  clickReligionWelshAnswerOther() {
    browser.element('[id="religion-welsh-answer-7"]').click()
    return this
  }

  setReligionWelshAnswerOtherText(value) {
    browser.setValue('[id="religion-welsh-answer-other"]', value)
    return this
  }

}

export default new ReligionPage()
