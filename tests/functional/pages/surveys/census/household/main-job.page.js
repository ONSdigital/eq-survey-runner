import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class MainJobPage extends MultipleChoiceWithOtherPage {

  clickAnEmployee() {
    browser.element('[id="main-job-answer-1"]').click()
    return this
  }

  clickSelfEmployedOrFreelanceWithoutEmployees() {
    browser.element('[id="main-job-answer-2"]').click()
    return this
  }

  clickSelfEmployedWithEmployees() {
    browser.element('[id="main-job-answer-3"]').click()
    return this
  }

}

export default new MainJobPage()
