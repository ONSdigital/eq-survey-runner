// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-12 22:01:11.918734 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class EmploymentTypePage extends MultipleChoiceWithOtherPage {

  clickEmploymentTypeAnswerWorkingAsAnEmployee() {
    browser.element('[id="employment-type-answer-1"]').click()
    return this
  }

  clickEmploymentTypeAnswerOnAGovernmentSponsoredTrainingScheme() {
    browser.element('[id="employment-type-answer-2"]').click()
    return this
  }

  clickEmploymentTypeAnswerSelfEmployedOrFreelance() {
    browser.element('[id="employment-type-answer-3"]').click()
    return this
  }

  clickEmploymentTypeAnswerWorkingPaidOrUnpaidForYouOwnOrYourFamilySBusiness() {
    browser.element('[id="employment-type-answer-4"]').click()
    return this
  }

  clickEmploymentTypeAnswerAwayFromWorkIllOnMaternityLeaveOnHolidayOrTemporarilyLaidOff() {
    browser.element('[id="employment-type-answer-5"]').click()
    return this
  }

  clickEmploymentTypeAnswerDoingAnyOtherKindOfPaidWork() {
    browser.element('[id="employment-type-answer-6"]').click()
    return this
  }

  clickEmploymentTypeAnswerNoneOfTheAbove() {
    browser.element('[id="employment-type-answer-7"]').click()
    return this
  }

}

export default new EmploymentTypePage()
