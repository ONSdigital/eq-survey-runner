const helpers = require('../helpers');
const TimeoutBlockPage = require('../generated_pages/timeout/timeout-block.page.js');

describe('Timeout', function() {
  it('Given I am completing an electronic questionnaire, when I have been inactive for the timeout period and attempt to submit data, then I will be redirected to a page confirming my session has timed out', function() {
    return helpers.openQuestionnaire('test_timeout.json').then(() => {
      return browser
          .pause(4000)
          .click(TimeoutBlockPage.submit())
          .getSource().should.eventually.contain('Your session has expired');
    });
  });
});
