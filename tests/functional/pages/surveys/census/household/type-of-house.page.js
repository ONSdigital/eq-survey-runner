import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class TypeOfHousePage extends MultipleChoiceWithOtherPage {

  clickDetached() {
    browser.element('[id="type-of-house-answer-1"]').click()
    return this
  }

  clickSemiDetached() {
    browser.element('[id="type-of-house-answer-2"]').click()
    return this
  }

  clickTerraced() {
    browser.element('[id="type-of-house-answer-3"]').click()
    return this
  }

}

export default new TypeOfHousePage()
