// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-14 14:19:14.067672 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class UsualResidentsPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('usual-residents')
  }

  clickUsualResidentsAnswerYes() {
    browser.element('[id="usual-residents-answer-1"]').click()
    return this
  }

  clickUsualResidentsAnswerNo() {
    browser.element('[id="usual-residents-answer-2"]').click()
    return this
  }

}

export default new UsualResidentsPage()
