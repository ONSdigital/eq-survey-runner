import chai from 'chai'
import {startQuestionnaire} from '../helpers'

import DatePage from '../pages/surveys/answers/date.page.js'

const expect = chai.expect

describe('Date range', function() {

  it('Given a date range option, a user should be able to click the label of each subfield to focus', function() {
    startQuestionnaire('test_date.json')
    DatePage.dayLabel.click()
    expect(browser.hasFocus(DatePage.dayInput.selector)).to.be.true
    DatePage.monthLabel.click()
    expect(browser.hasFocus(DatePage.monthInput.selector)).to.be.true
    DatePage.yearLabel.click()
    expect(browser.hasFocus(DatePage.yearInput.selector)).to.be.true
  })
})
