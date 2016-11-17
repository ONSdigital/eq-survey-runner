import QuestionPage from '../../question.page'

class EmploymentTypePage extends QuestionPage {

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

  setEmploymentTypeAnswer(value) {
    browser.setValue('[name="employment-type-answer"]', value)
    return this
  }

  getEmploymentTypeAnswer(value) {
    return browser.element('[name="employment-type-answer"]').getValue()
  }

}

export default new EmploymentTypePage()
