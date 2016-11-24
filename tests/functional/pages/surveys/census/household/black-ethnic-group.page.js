import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class BlackEthnicGroupPage extends MultipleChoiceWithOtherPage {

  clickAfrican() {
    browser.element('[id="black-ethnic-group-answer-1"]').click()
    return this
  }

  clickCaribbean() {
    browser.element('[id="black-ethnic-group-answer-2"]').click()
    return this
  }

  clickOther() {
    browser.element('[id="black-ethnic-group-answer-3"]').click()
    return this
  }

}

export default new BlackEthnicGroupPage()
