// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class DescribeResidentsPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('describe-residents')
  }

  clickDescribeResidentsAnswerFamilyMembers() {
    browser.element('[id="describe-residents-answer-0"]').click()
    return this
  }

  clickDescribeResidentsAnswerPayingGuests() {
    browser.element('[id="describe-residents-answer-1"]').click()
    return this
  }

  clickDescribeResidentsAnswerStaff() {
    browser.element('[id="describe-residents-answer-2"]').click()
    return this
  }

  clickDescribeResidentsAnswerOther() {
    browser.element('[id="describe-residents-answer-3"]').click()
    return this
  }

}

export default new DescribeResidentsPage()
