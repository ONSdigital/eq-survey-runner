import {expect} from 'chai'
import {openQuestionnaire, getRandomString} from '../helpers'
import TimeoutBlockPage from '../pages/surveys/timeout/timeout-block.page'
import TimeoutSummaryPage from '../pages/surveys/timeout/timeout-summary.page'

const dialog = '#dialog'

describe('Session timeout', function() {
  it('Given I am completing an electronic questionnaire, when I have been inactive for X minutes, and my session will timeout in 3 minutes time, then I will be informed that my session is going to expire (in 2 minutes) and will be able to see how long I have until the session expires', function() {
    openQuestionnaire('test_timeout.json')
    expect(browser.waitForVisible(dialog, 5000)).to.be.true
  })

  it('Given the timeout pop-up has appeared, when I choose to "Continue survey", then the pop-up will close and I am returned to the question I was last on with all data retained, and the timeout session resets to X minutes', function() {
    this.retries(3);
    openQuestionnaire('test_timeout.json')
    const pageUrl = browser.getUrl()
    browser.waitForVisible(dialog, 5000)
    // click 'Continue survey'
    browser.click('.js-timeout-continue')
    // expect page to be the same
    expect(browser.getUrl()).to.equal(pageUrl)
    // expect popup to not be visible
    browser.waitForVisible(dialog, 1000, true)
    expect(browser.isVisible(dialog)).to.be.false
    // expect popup to then be visible again (ie. timer has reset)
    expect(browser.waitForVisible(dialog, 5000)).to.be.true
  })

  it('Given the timeout pop-up has appeared, when I choose to "Save and sign out", then I am redirected to a page confirming I have been signed out and that all data saved will be retained ', function(done) {
    // Given
    let userId = getRandomString(10)
    let collectionId = getRandomString(10)
    openQuestionnaire('test_timeout.json', userId, collectionId)
    TimeoutBlockPage.setTimeoutAnswer('foo')
    browser.waitForVisible(dialog, 5000)

    // When
    browser.click('.js-timeout-save')

    // Then
    expect(browser.waitUntil(() => browser.getUrl().includes('signed-out'))).to.be.true
    openQuestionnaire('test_timeout.json', userId, collectionId)
    expect(TimeoutBlockPage.getTimeoutAnswer()).to.equal('foo')
  })

  it('Given the timeout pop-up has appeared, when I ignore it, then I will be signed out and redirected to a page confirming I have been signed out and that all data saved will be retained', function(done) {
    // Given
    let userId = getRandomString(10)
    let collectionId = getRandomString(10)
    openQuestionnaire('test_timeout.json', userId, collectionId)
    TimeoutBlockPage.setTimeoutAnswer('foo')
      .submit()

    // When
    expect(browser.waitUntil(() => browser.getUrl().includes('session-expired'), 7000)).to.be.true

    // Then
    openQuestionnaire('test_timeout.json', userId, collectionId)
    expect(TimeoutSummaryPage.isOpen(), 'Should resume on summary page').to.be.true
    expect(TimeoutSummaryPage.getTimeoutAnswer()).to.equal('foo')
  })

  it('Given I am on the summary page, when I click save and sign out, then I will be signed out and redirected to a page confirming I have been signed out', function(done) {
    // Given
    let userId = getRandomString(10)
    let collectionId = getRandomString(10)
    openQuestionnaire('test_timeout.json', userId, collectionId)
    TimeoutBlockPage.setTimeoutAnswer('foo')
      .submit()

    // When
    browser.waitForVisible(dialog, 5000)
    browser.click('.js-timeout-save')

    // Then
    expect(browser.getUrl()).to.contain('signed-out')
  })

})
