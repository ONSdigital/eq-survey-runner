import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class CarerPage extends MultipleChoiceWithOtherPage {

  clickNo() {
    browser.element('[id="carer-answer-1"]').click()
    return this
  }

  clickYes119HoursAWeek() {
    browser.element('[id="carer-answer-2"]').click()
    return this
  }

  clickYes2049HoursAWeek() {
    browser.element('[id="carer-answer-3"]').click()
    return this
  }

  clickYes50OrMoreHoursAWeek() {
    browser.element('[id="carer-answer-4"]').click()
    return this
  }

}

export default new CarerPage()
