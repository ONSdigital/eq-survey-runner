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

  setMainJobTypeAnswer(value) {
    browser.setValue('[name="main-job-type-answer"]', value)
    return this
  }

  getMainJobTypeAnswer(value) {
    return browser.element('[name="main-job-type-answer"]').getValue()
  }

}

export default new MainJobTypePage()
