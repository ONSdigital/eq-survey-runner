const helpers = require('../helpers');

const TimeoutBlockPage = require('../generated_pages/timeout/timeout-block.page.js');
const SummaryPage = require('../generated_pages/timeout/summary.page.js');

const dialog = '#dialog';

describe('Timeout', function() {

  it('Given I am completing an electronic questionnaire, when I have been inactive for X minutes, then I will be informed that my session is going to expire (in 2 minutes) and will be able to see how long I have until the session expires', function() {
    return helpers.openQuestionnaire('test_timeout.json').then(() => {
        return browser
          .waitForVisible(dialog,5000);
    });
  });

  it('Given the timeout pop-up has appeared, when I choose to "Continue survey", then the pop-up will close and I am returned to the question I was last on with all data retained, and the timeout session resets to X minutes', function() {
    return helpers.openQuestionnaire('test_timeout.json').then(() => {
        return browser
          .waitForVisible(dialog,5000)
          .click('.js-timeout-continue')
          .getUrl().should.eventually.contain(TimeoutBlockPage.pageName)
          .waitForVisible(dialog,1000, true)
          .isVisible(dialog).should.eventually.be.false
          .waitForVisible(dialog,5000);
    });
  });

  it('Given the timeout pop-up has appeared, when I choose to "Save and sign out", then I am redirected to a page confirming I have been signed out and that all data saved will be retained', function() {
    const collectionId = helpers.getRandomString(10);
    return helpers.openQuestionnaire('test_timeout.json', 'testUser', collectionId).then(() => {
      return browser
        .setValue(TimeoutBlockPage.timeout(), 'foo')
        .waitForVisible(dialog,5000)
        .click('.js-timeout-save')
        .getUrl().should.eventually.contain('signed-out');
    })
    .then(() => {
      return helpers.openQuestionnaire('test_timeout.json', 'testUser', collectionId);
    })
    .then(() => {
      return browser
        .getValue(TimeoutBlockPage.timeout()).should.eventually.equal('foo');
    });
  });

  it('Given the timeout pop-up has appeared, when I ignore it, then I will be signed out and redirected to a page confirming I have been signed out and that all data saved will be retained', function() {
    const collectionId = helpers.getRandomString(10);
    return helpers.openQuestionnaire('test_timeout.json', 'testUser', collectionId).then(() => {
      return browser
        .setValue(TimeoutBlockPage.timeout(), 'foo')
        .click(TimeoutBlockPage.submit())
        .waitUntil(() => browser.getUrl().should.eventually.contain('session-expired'), 7000);
    })
    .then(() => {
      return helpers.openQuestionnaire('test_timeout.json', 'testUser', collectionId);
    })
    .then(() => {
      return browser
        .getUrl().should.eventually.contain('summary')
        .getText(SummaryPage.timeoutAnswer()).should.eventually.contain('foo');
    });
  });

  it('Given I am on the summary page, when I click save and sign out, then I will be signed out and redirected to a page confirming I have been signed out', function() {
    return helpers.openQuestionnaire('test_timeout.json').then(() => {
      return browser
        .setValue(TimeoutBlockPage.timeout(), 'foo')
        .click(TimeoutBlockPage.submit())
        .getUrl().should.eventually.contain('summary')
        .waitForVisible(dialog,5000)
        .click('.js-timeout-save')
        .getUrl().should.eventually.contain('signed-out');
    });
  });

});
