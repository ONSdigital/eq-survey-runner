import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class CarerPage extends MultipleChoiceWithOtherPage {

  clickCarerAnswerNo() {
    browser.element('[id="carer-answer-1"]').click()
    return this
  }

  clickCarerAnswerYes119HoursAWeek() {
    browser.element('[id="carer-answer-2"]').click()
    return this
  }

  clickCarerAnswerYes2049HoursAWeek() {
    browser.element('[id="carer-answer-3"]').click()
    return this
  }

  clickCarerAnswerYes50OrMoreHoursAWeek() {
    browser.element('[id="carer-answer-4"]').click()
    return this
  }

}

export default new CarerPage()
