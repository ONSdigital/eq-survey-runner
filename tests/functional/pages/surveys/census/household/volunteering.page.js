// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.835425 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class VolunteeringPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('volunteering')
  }

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
