import assert from 'assert'
import { expect } from 'chai'
import { startQuestionnaire } from '../helpers'
import devPage from '../pages/dev.page'

describe('Census theme', function() {

  it('Given the census theme is selected, the help should not be visible', function() {
    // Given
    startQuestionnaire('census_theme.json')
    // Then
    expect(browser.isVisible('.js-help-body')).to.be.false
  })

  it('Given the census theme is selected, and I click the "help and support" button the help should be visible', function() {
    // When
    browser.click('.js-help-btn')
    // Then
    expect(browser.isVisible('.js-help-body')).to.be.true
  })

})
