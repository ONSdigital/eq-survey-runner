import {expect} from 'chai'
import {openQuestionnaire} from '../helpers'

const dialog = '#dialog'

describe('Session timeout', function() {
  it('Given I am completing an electronic questionnaire, when I have been inactive for X minutes, and my session will timeout in 3 minutes time, then I will be informed that my session is going to expire (in 2 minutes) and will be able to see how long I have until the session expires', function() {
    openQuestionnaire('test_timeout.json')
    expect(browser.waitForVisible(dialog, 5000)).to.be.true
  })

  it('Given the timeout pop-up has appeared, when I choose to "Continue survey", then the pop-up will close and I am returned to the question I was last on with all data retained, and the timeout session resets to X minutes', function() {
    openQuestionnaire('test_timeout.json')
    const pageUrl = browser.getUrl()
    browser.waitForVisible(dialog, 5000)
    // click 'Continue survey'
    browser.click('.js-timeout-continue')
    // expect page to be the same
    expect(browser.getUrl()).to.equal(pageUrl)
    // expect popup to not be visible
    expect(browser.isVisible(dialog)).to.be.false
    // expect popup to then be visible again (ie. timer has reset)
    expect(browser.waitForVisible(dialog, 5000)).to.be.true
  })

  it('Given the timeout pop-up has appeared, when I choose to "Save and sign out", then I am redirected to a page confirming I have been signed out and that all data saved will be retained ', function(done) {
    openQuestionnaire('test_timeout.json')
    browser.waitForVisible(dialog, 5000)
    browser.click('.js-timeout-save')
    expect(browser.waitUntil(() => browser.getUrl().includes('signed-out'))).to.be.true
  })

  it('Given the timeout pop-up has appeared, when I ignore it, then I will be signed out and redirected to a page confirming I have been signed out and that all data saved will be retained', function(done) {
    openQuestionnaire('test_timeout.json')
    expect(browser.waitUntil(() => browser.getUrl().includes('session-expired'), 7000)).to.be.true
  })

})
