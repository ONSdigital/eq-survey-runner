// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.866648 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class MainJobTypePage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('main-job-type')
  }

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
