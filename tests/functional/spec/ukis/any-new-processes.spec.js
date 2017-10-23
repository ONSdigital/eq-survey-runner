const helpers = require('../../helpers');

const ProcessImproved = require('../../pages/surveys/ukis/process-improved.page.js');
const ProcessInnovationCompleted = require('../../pages/surveys/ukis/process-innovation-completed.page.js');

describe('Example Test', function() {

  it('Given I am answering question 5.1 under 5. Process Innovation block, When I don\'t select or select No as the response, Then I am routed to interstitial page', function() {
    return helpers.startQuestionnaire('1_0001.json').then(() => {
        return browser

        .click(helpers.navigationLink('Process Innovation'))
        .getUrl().should.eventually.contain(ProcessImproved.pageName)
        // when submit without a response
        .click(ProcessImproved.submit())
        .getUrl().should.eventually.contain(ProcessInnovationCompleted.pageName)
        .click(ProcessInnovationCompleted.previous())

        // when No selected
        .click(ProcessImproved.no())
        .click(ProcessImproved.submit())
        .getUrl().should.eventually.contain(ProcessInnovationCompleted.pageName);
    });
  });

});
