// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-14 14:19:14.072036 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class DescribeResidentsPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('describe-residents')
  }

  clickDescribeResidentsAnswerFamilyMembers() {
    browser.element('[id="describe-residents-answer-1"]').click()
    return this
  }

  clickDescribeResidentsAnswerPayingGuests() {
    browser.element('[id="describe-residents-answer-2"]').click()
    return this
  }

  clickDescribeResidentsAnswerStaff() {
    browser.element('[id="describe-residents-answer-3"]').click()
    return this
  }

  clickDescribeResidentsAnswerOther() {
    browser.element('[id="describe-residents-answer-4"]').click()
    return this
  }

}

export default new DescribeResidentsPage()
