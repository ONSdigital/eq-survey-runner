import QuestionPage from '../../question.page'

class ReligionPage extends QuestionPage {

  clickNoReligion() {
    browser.element('[id="religion-answer-1"]').click()
    return this
  }

  clickChristianIncludingChurchOfEnglandCatholicProtestantAndAllOtherChristianDenominations() {
    browser.element('[id="religion-answer-2"]').click()
    return this
  }

  clickBuddhist() {
    browser.element('[id="religion-answer-3"]').click()
    return this
  }

  clickHindu() {
    browser.element('[id="religion-answer-4"]').click()
    return this
  }

  clickJewish() {
    browser.element('[id="religion-answer-5"]').click()
    return this
  }

  clickMuslim() {
    browser.element('[id="religion-answer-6"]').click()
    return this
  }

  clickSikh() {
    browser.element('[id="religion-answer-7"]').click()
    return this
  }

  clickOther() {
    browser.element('[id="religion-answer-8"]').click()
    return this
  }

  setReligionAnswer(value) {
    browser.setValue('[name="religion-answer"]', value)
    return this
  }

  getReligionAnswer(value) {
    return browser.element('[name="religion-answer"]').getValue()
  }

  clickNoReligion() {
    browser.element('[id="religion-welsh-answer-1"]').click()
    return this
  }

  clickChristianAllDenominations() {
    browser.element('[id="religion-welsh-answer-2"]').click()
    return this
  }

  clickBuddhist() {
    browser.element('[id="religion-welsh-answer-3"]').click()
    return this
  }

  clickHindu() {
    browser.element('[id="religion-welsh-answer-4"]').click()
    return this
  }

  clickJewish() {
    browser.element('[id="religion-welsh-answer-5"]').click()
    return this
  }

  clickMuslim() {
    browser.element('[id="religion-welsh-answer-6"]').click()
    return this
  }

  clickSikh() {
    browser.element('[id="religion-welsh-answer-7"]').click()
    return this
  }

  clickOther() {
    browser.element('[id="religion-welsh-answer-8"]').click()
    return this
  }

  setReligionWelshAnswer(value) {
    browser.setValue('[name="religion-welsh-answer"]', value)
    return this
  }

  getReligionWelshAnswer(value) {
    return browser.element('[name="religion-welsh-answer"]').getValue()
  }

}

export default new ReligionPage()
