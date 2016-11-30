import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class LengthOfStayPage extends MultipleChoiceWithOtherPage {

  clickLengthOfStayAnswerLessThan6Months() {
    browser.element('[id="length-of-stay-answer-1"]').click()
    return this
  }

  clickLengthOfStayAnswer6MonthsOrMoreButLessThan12Months() {
    browser.element('[id="length-of-stay-answer-2"]').click()
    return this
  }

  clickLengthOfStayAnswer12MonthsOrMore() {
    browser.element('[id="length-of-stay-answer-3"]').click()
    return this
  }

}

export default new LengthOfStayPage()
