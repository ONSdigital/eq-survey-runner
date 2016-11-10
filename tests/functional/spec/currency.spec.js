import chai from 'chai'
import {startQuestionnaire} from '../helpers'

import TextFieldPage from '../pages/surveys/answers/textfield.page.js'

const expect = chai.expect

describe('Currency', function() {

  it('Given a currency option, a user should be able to click the label of the currency field to focus', function() {
    startQuestionnaire('test_currency.json')
    TextFieldPage.label.click()
    expect(browser.hasFocus(TextFieldPage.textfield.selector)).to.be.true
  })
})
