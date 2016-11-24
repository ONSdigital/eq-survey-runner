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

}

export default new LengthOfStayPage()
