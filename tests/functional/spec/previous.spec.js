const helpers = require('../helpers');
const EmploymentStatusBlockPage = require('../generated_pages/hub_and_spoke/employment-status.page.js');
const HubPage = require('../base_pages/hub.page.js');
const schema = 'test_hub_complete_sections.json';

describe('Choose another section link', function () {

  it('When a user gets to initial question, then the previous location link should not be displayed', function () {
    return helpers.openQuestionnaire(schema)
      .then(() => {
        return browser
          .getSource().should.not.eventually.contain('Previous link click');

      });
  });

  it('When a user gets to the hub, then the previous location link should not be displayed', function () {
    return helpers.openQuestionnaire(schema)
      .then(() => {
        return browser
          .click(EmploymentStatusBlockPage.workingAsAnEmployee())
          .click(EmploymentStatusBlockPage.submit())
          .getSource().should.not.eventually.contain('Previous link click');

      });
  });

  it('When a user gets to subsequent question, then the previous location link should be displayed', function () {
    return helpers.openQuestionnaire(schema)
      .then(() => {
        return browser
          .click(EmploymentStatusBlockPage.exclusiveNoneOfTheseApply())
          .click(EmploymentStatusBlockPage.submit())
          .getSource().should.eventually.contain('Previous link click');

      });
  });

  it('When a user gets to subsequent questions past the hub, then the previous location link should be displayed', function () {
    return helpers.openQuestionnaire(schema)
      .then(() => {
        return browser
          .click(EmploymentStatusBlockPage.workingAsAnEmployee())
          .click(EmploymentStatusBlockPage.submit())
          .click(HubPage.summaryRowLink(2))
          .getSource().should.eventually.contain('Previous link click');

      });
  });
});
