// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-12 22:01:11.945862 - DO NOT EDIT!!! <<<

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
