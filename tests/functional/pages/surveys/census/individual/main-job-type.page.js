// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class MainJobTypePage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('main-job-type')
  }

  clickMainJobTypeAnswerEmployedByAnOrganisationOrBusiness() {
    browser.element('[id="main-job-type-answer-0"]').click()
    return this
  }

  clickMainJobTypeAnswerSelfEmployedInYourOwnOrganisationOrBusiness() {
    browser.element('[id="main-job-type-answer-1"]').click()
    return this
  }

  clickMainJobTypeAnswerNotWorkingForAnOrganisationOrBusiness() {
    browser.element('[id="main-job-type-answer-2"]').click()
    return this
  }

}

export default new MainJobTypePage()
