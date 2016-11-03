class TextFieldPage {
  get label() {
    return browser.element('#label-answer')
  }

  get textfield() {
    return browser.element('#input-answer')
  }
}

export default new TextFieldPage()
