import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class MainJobTypePage extends MultipleChoiceWithOtherPage {

  clickMainJobTypeAnswerEmployedByAnOrganisationOrBusiness() {
    browser.element('[id="main-job-type-answer-1"]').click()
    return this
  }

  clickMainJobTypeAnswerSelfEmployedInYourOwnOrganisationOrBusiness() {
    browser.element('[id="main-job-type-answer-2"]').click()
    return this
  }

  clickMainJobTypeAnswerNotWorkingForAnOrganisationOrBusiness() {
    browser.element('[id="main-job-type-answer-3"]').click()
    return this
  }

}

export default new MainJobTypePage()
