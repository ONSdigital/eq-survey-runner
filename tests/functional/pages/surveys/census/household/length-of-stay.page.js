import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class LengthOfStayPage extends MultipleChoiceWithOtherPage {

  clickLessThan6Months() {
    browser.element('[id="length-of-stay-answer-1"]').click()
    return this
  }

  click6MonthsOrMoreButLessThan12Months() {
    browser.element('[id="length-of-stay-answer-2"]').click()
    return this
  }

  click12MonthsOrMore() {
    browser.element('[id="length-of-stay-answer-3"]').click()
    return this
  }

  setLengthOfStayAnswer(value) {
    browser.setValue('[name="length-of-stay-answer"]', value)
    return this
  }

  getLengthOfStayAnswer(value) {
    return browser.element('[name="length-of-stay-answer"]').getValue()
  }

}

export default new LengthOfStayPage()
