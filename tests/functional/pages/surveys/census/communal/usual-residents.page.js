import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class UsualResidentsPage extends MultipleChoiceWithOtherPage {

  clickUsualResidentsAnswerYes() {
    browser.element('[id="usual-residents-answer-1"]').click()
    return this
  }

  clickUsualResidentsAnswerNo() {
    browser.element('[id="usual-residents-answer-2"]').click()
    return this
  }

}

export default new UsualResidentsPage()
