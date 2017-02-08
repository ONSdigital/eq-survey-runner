// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class SignificantEventsPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('significant-events')
  }

  clickSignificantEventsEstablishedAnswerYes() {
    browser.element('[id="significant-events-established-answer-0"]').click()
    return this
  }

  clickSignificantEventsEstablishedAnswerNo() {
    browser.element('[id="significant-events-established-answer-1"]').click()
    return this
  }

  clickSignificantEventsTurnoverIncreaseAnswerYes() {
    browser.element('[id="significant-events-turnover-increase-answer-0"]').click()
    return this
  }

  clickSignificantEventsTurnoverIncreaseAnswerNo() {
    browser.element('[id="significant-events-turnover-increase-answer-1"]').click()
    return this
  }

  clickSignificantEventsTurnoverDecreaseAnswerYes() {
    browser.element('[id="significant-events-turnover-decrease-answer-0"]').click()
    return this
  }

  clickSignificantEventsTurnoverDecreaseAnswerNo() {
    browser.element('[id="significant-events-turnover-decrease-answer-1"]').click()
    return this
  }

}

export default new SignificantEventsPage()
