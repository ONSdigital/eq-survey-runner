import {openQuestionnaire} from '../helpers'

import TextFieldPage from '../pages/surveys/answers/textfield.page.js'


describe('Textfield', function() {

  it('Given a textfield option, a user should be able to click the label of the textfield to focus', function() {
    openQuestionnaire('test_textfield.json')
    TextFieldPage.label.click()
    expect(browser.hasFocus(TextFieldPage.textfield.selector)).to.be.true
  })
})
