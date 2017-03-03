import {openQuestionnaire} from '../helpers'

import TextFieldPage from '../pages/surveys/answers/textfield.page.js'


describe('Currency', function() {

  it('Given a currency option, a user should be able to click the label of the currency field to focus', function() {
    openQuestionnaire('test_currency.json')
    TextFieldPage.label.click()
    expect(browser.hasFocus(TextFieldPage.textfield.selector)).to.be.true
  })
})
