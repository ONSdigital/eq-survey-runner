// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FortnightlyPaySignificantChangesOvertimePage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('fortnightly-pay-significant-changes-overtime')
  }

  clickFortnightlyPaySignificantChangesOvertimeAnswerMoreOvertime() {
    browser.element('[id="fortnightly-pay-significant-changes-overtime-answer-0"]').click()
    return this
  }

  clickFortnightlyPaySignificantChangesOvertimeAnswerLessOvertime() {
    browser.element('[id="fortnightly-pay-significant-changes-overtime-answer-1"]').click()
    return this
  }

  clickFortnightlyPaySignificantChangesOvertimeAnswerNoSignificantChange() {
    browser.element('[id="fortnightly-pay-significant-changes-overtime-answer-2"]').click()
    return this
  }

}

export default new FortnightlyPaySignificantChangesOvertimePage()
