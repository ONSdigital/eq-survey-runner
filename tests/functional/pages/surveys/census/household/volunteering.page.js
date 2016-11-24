import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class VolunteeringPage extends MultipleChoiceWithOtherPage {

  clickNo() {
    browser.element('[id="volunteering-answer-1"]').click()
    return this
  }

  clickYesAtLeastOnceAWeek() {
    browser.element('[id="volunteering-answer-2"]').click()
    return this
  }

  clickYesLessThanOnceAWeekButAtLeastOnceAMonth() {
    browser.element('[id="volunteering-answer-3"]').click()
    return this
  }

  clickYesLessOften() {
    browser.element('[id="volunteering-answer-4"]').click()
    return this
  }

}

export default new VolunteeringPage()
