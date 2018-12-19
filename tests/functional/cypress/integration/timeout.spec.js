import {openQuestionnaire} from '../helpers/helpers.js'

const TimeoutBlockPage = require('../generated_pages/timeout/timeout-block.page.js');
const SummaryPage = require('../generated_pages/timeout/summary.page.js');

const dialog = '#dialog';

describe('Timeout', function() {

  it('Given I am completing an electronic questionnaire, when I have been inactive for X minutes, then I will be informed that my session is going to expire (in 2 minutes) and will be able to see how long I have until the session expires', function() {
    openQuestionnaire('test_timeout.json')
                  .waitForVisible(dialog,5000);
    });
  });

  it('Given the timeout pop-up has appeared, when I choose to "Continue survey", then the pop-up will close and I am returned to the question I was last on with all data retained, and the timeout session resets to X minutes', function() {
    openQuestionnaire('test_timeout.json')
                  .waitForVisible(dialog,5000)
          .get('.js-timeout-continue').click()
          .url().should('contain', TimeoutBlockPage.pageName)
          .waitForVisible(dialog,1000, true)
          .get(dialog).should('not.be.visible')
          .waitForVisible(dialog,5000);
    });
  });

  it('Given the timeout pop-up has appeared, when I choose to "Save and sign out", then I am redirected to a page confirming I have been signed out and that all data saved will be retained', function() {
    const collectionId = helpers.getRandomString(10);
    openQuestionnaire('test_timeout.json', { userId: 'testUser', collectionId: collectionId })
              .get(TimeoutBlockPage.timeout()).type('foo')
        .waitForVisible(dialog,5000)
        .get('.js-timeout-save').click()
        .url().should('contain', 'localhost');
    })
    .then(() => {
      return helpers.openQuestionnaire('test_timeout.json', { userId: 'testUser', collectionId: collectionId });
    })
    .then(() => {
              .getValue(TimeoutBlockPage.timeout()).should.eventually.equal('foo');
    });
  });

  it('Given the timeout pop-up has appeared, when I ignore it, then I will be signed out and redirected to a page confirming I have been signed out and that all data saved will be retained', function() {
    const collectionId = helpers.getRandomString(10);
    openQuestionnaire('test_timeout.json', { userId: 'testUser', collectionId: collectionId })
              .get(TimeoutBlockPage.timeout()).type('foo')
        .get(TimeoutBlockPage.submit()).click()
        .waitUntil(() => browser.url().should('contain', 'session-expired'), 7000);
    })
    .then(() => {
      return helpers.openQuestionnaire('test_timeout.json', { userId: 'testUser', collectionId: collectionId });
    })
    .then(() => {
              .url().should('contain', 'summary')
        .get(SummaryPage.timeoutAnswer()).stripText().should('contain', 'foo');
    });
  });

  it('Given I am on the summary page, when I click save and sign out, then I will be signed out and redirected to a page confirming I have been signed out', function() {
    openQuestionnaire('test_timeout.json')
              .get(TimeoutBlockPage.timeout()).type('foo')
        .get(TimeoutBlockPage.submit()).click()
        .url().should('contain', 'summary')
        .waitForVisible(dialog,5000)
        .get('.js-timeout-save').click()
        .url().should('contain', 'localhost');
    });
  });

});
