const EmploymentStatusBlockPage = require('../../../generated_pages/hub_and_spoke/employment-status.page.js');
const EmploymentTypePage = require('../../../generated_pages/hub_and_spoke/employment-type.page.js');
const HubPage = require('../../../base_pages/hub.page.js');
const ProxyPage = require('../../../generated_pages/hub_and_spoke/proxy.page.js');
const schema = 'test_hub_complete_sections.json';

describe('Choose another section link', function () {
  beforeEach(function() {
    browser.openQuestionnaire(schema);
  });

  it('When a user gets to initial question, then the previous location link should not be displayed', function () {
    expect($(EmploymentStatusBlockPage.previous()).isExisting()).to.be.false;
  });

  it('When a user gets to the hub, then the previous location link should not be displayed', function () {
    $(EmploymentStatusBlockPage.workingAsAnEmployee()).click();
    $(EmploymentStatusBlockPage.submit()).click();
    expect($(HubPage.previous()).isExisting()).to.be.false;
  });

  it('When a user gets to subsequent question, then the previous location link should be displayed', function () {
    $(EmploymentStatusBlockPage.exclusiveNoneOfTheseApply()).click();
    $(EmploymentStatusBlockPage.submit()).click();
    expect($(EmploymentTypePage.previous()).isExisting()).to.be.true;
  });

  it('When a user gets to subsequent questions past the hub, then the previous location link should be displayed', function () {
    $(EmploymentStatusBlockPage.workingAsAnEmployee()).click();
    $(EmploymentStatusBlockPage.submit()).click();
    $(HubPage.summaryRowLink(2)).click();
    expect($(ProxyPage.previous()).isExisting()).to.be.true;
  });
});
