import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class EmploymentTypePage extends MultipleChoiceWithOtherPage {

  clickWorkingAsAnEmployee() {
    browser.element('[id="employment-type-answer-1"]').click()
    return this
  }

  clickOnAGovernmentSponsoredTrainingScheme() {
    browser.element('[id="employment-type-answer-2"]').click()
    return this
  }

  clickSelfEmployedOrFreelance() {
    browser.element('[id="employment-type-answer-3"]').click()
    return this
  }

  clickWorkingPaidOrUnpaidForYouOwnOrYourFamilySBusiness() {
    browser.element('[id="employment-type-answer-4"]').click()
    return this
  }

  clickAwayFromWorkIllOnMaternityLeaveOnHolidayOrTemporarilyLaidOff() {
    browser.element('[id="employment-type-answer-5"]').click()
    return this
  }

  clickDoingAnyOtherKindOfPaidWork() {
    browser.element('[id="employment-type-answer-6"]').click()
    return this
  }

  clickNoneOfTheAbove() {
    browser.element('[id="employment-type-answer-7"]').click()
    return this
  }

}

export default new EmploymentTypePage()
