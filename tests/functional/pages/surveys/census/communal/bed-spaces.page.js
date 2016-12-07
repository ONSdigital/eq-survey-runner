import QuestionPage from '../../question.page'

class BedSpacesPage extends QuestionPage {

  setBedSpacesAnswer(value) {
    browser.setValue('[name="bed-spaces-answer"]', value)
    return this
  }

  getBedSpacesAnswer(value) {
    return browser.element('[name="bed-spaces-answer"]').getValue()
  }

}

export default new BedSpacesPage()
