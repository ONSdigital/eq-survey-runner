import {expect} from 'chai'
import {openQuestionnaire, landingPage} from '../helpers'
const SESSION_TIMEOUT = 'sessionTimeout'
const SESSION_PROMPT_TIME = 'sessionPromptTime'

const dialog = '#dialog'

const startSurveyWithTimeoutConfig = (sessionTimeout = 10, sessionPromptTime = 5) => {
  openQuestionnaire('1_0001.json')
  browser.sessionStorage('POST', {key: SESSION_TIMEOUT, value: sessionTimeout.toString()})
  browser.sessionStorage('POST', {key: SESSION_PROMPT_TIME, value: sessionPromptTime.toString()})
  landingPage.getStarted()
}

describe('Session timeout', function() {
  it('Given I am completing an electronic questionnaire, when I have been inactive for X minutes, and my session will timeout in 3 minutes time, then I will be informed that my session is going to expire (in 2 minutes) and will be able to see how long I have until the session expires', function() {
    startSurveyWithTimeoutConfig()
    // expect dialog to not be visible after 3 seconds
    expect(browser.waitForVisible(dialog, 3000, true)).to.be.true
    expect(browser.waitForVisible(dialog, 7000)).to.be.true
  })

  it('Given the timeout pop-up has appeared, when I choose to "Continue survey", then the pop-up will close and I am returned to the question I was last on with all data retained, and the timeout session resets to X minutes', function() {
    startSurveyWithTimeoutConfig()
    const pageUrl = browser.getUrl()
    browser.waitForVisible(dialog, 7000)
    // click 'Continue survey'
    browser.click('.js-timeout-continue')
    // expect popup to not be visible after 1 seconds
    expect(browser.waitForVisible(dialog, 1000, true)).to.be.true
    // expect page to be the same
    expect(browser.getUrl()).to.equal(pageUrl)
    // expect popoup to still not be visible after 3 seconds
    expect(browser.waitForVisible(dialog, 3000, true)).to.be.true
    // expect popup to then be visible again (ie. timer has reset)
    expect(browser.waitForVisible(dialog, 7000)).to.be.true
  })

  it('Given the timeout pop-up has appeared, when I choose to "Save and sign out", then I am redirected to a page confirming I have been signed out and that all data saved will be retained ', function(done) {
    startSurveyWithTimeoutConfig(10, 9)
    browser.waitForVisible(dialog, 3000)
    browser.click('.js-timeout-save')
    expect(browser.waitUntil(() => browser.getUrl().includes('signed-out'), 5000)).to.be.true
  })

  it('Given the timeout pop-up has appeared, when I ignore it, then after 2 minutes I will be signed out, and I am redirected to a page confirming I have been signed out and that all data saved will be retained', function(done) {
    startSurveyWithTimeoutConfig(1, 1)
    expect(browser.waitUntil(() => browser.getUrl().includes('session-expired'), 5000)).to.be.true
  })

  it('Given I completing the UKIS survey, when the timeout warning appears, then clocking the "Save and sign out" button should sign me out', function(done) {
    startSurveyWithTimeoutConfig(10, 9)
    browser.waitForVisible(dialog, 3000)
    browser.click('.js-timeout-save')
    expect(browser.waitUntil(() => browser.getUrl().includes('signed-out'), 5000)).to.be.true
  })

  it('Given the timeout pop-up has appeared, when I ignore it, then after 2 minutes I will be signed out, and I am redirected to a page confirming I have been signed out and that all data saved will be retained', function(done) {
    startSurveyWithTimeoutConfig(1, 1)
    expect(browser.waitUntil(() => browser.getUrl().includes('session-expired'), 5000)).to.be.true
  })

})
