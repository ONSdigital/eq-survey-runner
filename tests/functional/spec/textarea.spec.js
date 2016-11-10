import chai from 'chai'
import {startQuestionnaire} from '../helpers'

import TextFieldPage from '../pages/surveys/answers/textfield.page.js'

const expect = chai.expect

describe('Textarea', function() {

  it('Given a textarea option, a user should be able to click the label of the textarea to focus', function() {
    startQuestionnaire('test_textarea.json')
    TextFieldPage.label.click()
    expect(browser.hasFocus(TextFieldPage.textfield.selector)).to.be.true
  })
})
