const helpers = require('../../../helpers');

const EmploymentStatusBlockPage = require('../../../generated_pages/hub_and_spoke/employment-status.page.js');
const EmploymentTypeBlockPage = require('../../../generated_pages/hub_and_spoke/employment-type.page.js');

const ProxyPage = require('../../../generated_pages/hub_and_spoke/proxy.page.js');
const AccomodationDetailsSummaryBlockPage = require('../../../generated_pages/hub_and_spoke/accommodation-details-summary.page.js');

const HubPage = require('../../../base_pages/hub.page.js');

describe('Choose another section', function () {
    it('When I open the first question, then the \'Chose another section\' link should not be displayed', function () {
        return helpers.openQuestionnaire("test_hub_complete_sections").then(() => {
        return browser
             .getText('body').should.not.eventually.have.string('Can\'t complete this question?');
      });
 });
