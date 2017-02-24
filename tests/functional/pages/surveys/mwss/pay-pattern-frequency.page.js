// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class PayPatternFrequencyPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('pay-pattern-frequency')
  }

  clickPayPatternFrequencyAnswerWeekly() {
    browser.element('[id="pay-pattern-frequency-answer-0"]').click()
    return this
  }

  clickPayPatternFrequencyAnswerFortnightly() {
    browser.element('[id="pay-pattern-frequency-answer-1"]').click()
    return this
  }

  clickPayPatternFrequencyAnswerCalendarMonthly() {
    browser.element('[id="pay-pattern-frequency-answer-2"]').click()
    return this
  }

  clickPayPatternFrequencyAnswerFourWeekly() {
    browser.element('[id="pay-pattern-frequency-answer-3"]').click()
    return this
  }

  clickPayPatternFrequencyAnswerFiveWeekly() {
    browser.element('[id="pay-pattern-frequency-answer-4"]').click()
    return this
  }

}

export default new PayPatternFrequencyPage()
