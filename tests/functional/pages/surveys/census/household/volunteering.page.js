// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-12 22:01:11.917364 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class VolunteeringPage extends MultipleChoiceWithOtherPage {

  clickVolunteeringAnswerNo() {
    browser.element('[id="volunteering-answer-1"]').click()
    return this
  }

  clickVolunteeringAnswerYesAtLeastOnceAWeek() {
    browser.element('[id="volunteering-answer-2"]').click()
    return this
  }

  clickVolunteeringAnswerYesLessThanOnceAWeekButAtLeastOnceAMonth() {
    browser.element('[id="volunteering-answer-3"]').click()
    return this
  }

  clickVolunteeringAnswerYesLessOften() {
    browser.element('[id="volunteering-answer-4"]').click()
    return this
  }

}

export default new VolunteeringPage()
