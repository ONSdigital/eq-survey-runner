import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class MainJobTypePage extends MultipleChoiceWithOtherPage {

  clickEmployedByAnOrganisationOrBusiness() {
    browser.element('[id="main-job-type-answer-1"]').click()
    return this
  }

  clickSelfEmployedInYourOwnBusiness() {
    browser.element('[id="main-job-type-answer-2"]').click()
    return this
  }

  clickNotWorkingForAnOrganisation() {
    browser.element('[id="main-job-type-answer-3"]').click()
    return this
  }

}

export default new MainJobTypePage()
