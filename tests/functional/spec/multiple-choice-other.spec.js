import chai from 'chai'
import {startQuestionnaire} from '../helpers'

const expect = chai.expect

describe('Multiple choice "other" option', function() {

  before(function() {
    startQuestionnaire('0_checkbox_other.json')
  })

  it('Given an "other" option is available, when the user clicks the "other" option the other input should be visible', function() {
    browser.click('[data-qa="has-other-option"]')
    expect(browser.isVisible('[data-qa="other-option"]')).to.be.true
  })

})
