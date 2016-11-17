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

  setVolunteeringAnswer(value) {
    browser.setValue('[name="volunteering-answer"]', value)
    return this
  }

  getVolunteeringAnswer(value) {
    return browser.element('[name="volunteering-answer"]').getValue()
  }

}

export default new VolunteeringPage()
